<template>
  <div>
    <el-row>
      <el-col :span="21">
        <el-input
          placeholder="输入订单号查询订单"
          size="mini"
          style="width: 25em;"
          v-model="order_id"
          onkeyup="value = value.replace(/[^\d]/g,'');"
        >
          <el-button slot="append" icon="el-icon-search" @click="query_order()"></el-button>
        </el-input>
      </el-col>
      <el-col :span="3" style="color: grey;">
        <span v-if="loading">
          <i class="el-icon-loading" slot="suffix"></i>加载中...
        </span>
      </el-col>
    </el-row>
    <el-divider></el-divider>
    <div style="height: 29em; width: 51em;">
      <el-row>
        <el-table
          :data="orders"
          height="39em"
          ref="table"
          size="mini"
          :header-cell-style="{background:'#eef1f6',color:'#606266', 'text-align': 'center'}"
          style="overflow-anchor:none;"
        >
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-table
                :data="props.row.skus"
                size="mini"
                :header-cell-style="{background:'#eef1f6',color:'#606266', 'text-align': 'center'}"
              >
                <el-table-column align="center" width="90">
                  <template slot-scope="scope">
                    <el-image
                      :src="scope.row.sku.default_image_url"
                      style="width: 5em; height: 5em;"
                    ></el-image>
                  </template>
                </el-table-column>
                <el-table-column label="商品名称" width="250">
                  <template slot-scope="scope">{{ scope.row.sku.name }}</template>
                </el-table-column>
                <el-table-column align="center" label="规格" prop="spec" width="120"></el-table-column>
                <el-table-column align="center" label="数量" prop="count" width="80"></el-table-column>
                <el-table-column align="center" label="价格" prop="price" width="100"></el-table-column>
                <el-table-column align="center" label="历史评分" prop="score" width="80"></el-table-column>
              </el-table>
            </template>
          </el-table-column>
          <el-table-column align="center" label="序号" width="80" type="index"></el-table-column>
          <el-table-column align="center" label="订单号" prop="order_id" width="160"></el-table-column>
          <el-table-column align="center" label="数量" prop="total_count" width="80"></el-table-column>
          <el-table-column align="center" label="总金额" prop="total_amount" width="120"></el-table-column>
          <el-table-column align="center" label="订单运费" prop="freight" width="120"></el-table-column>
          <el-table-column align="center" label="订单状态" prop="status_text" width="85"></el-table-column>
          <el-table-column align="center" label="操作" width="120">
            <template slot-scope="scope">
              <el-button
                type="primary"
                size="mini"
                v-if="scope.row.status == 1"
                @click="pay_order(scope.row.order_id)"
              >去支付</el-button>
              <el-button type="primary" size="mini" v-if="scope.row.status == 2">去催单</el-button>
              <el-button type="primary" size="mini" v-if="scope.row.status == 3">确认收货</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-row>
    </div>
  </div>
</template>
<script>
/* eslint-disable */
export default {
  name: "Orders",
  data() {
    return {
      // 订单
      orders: [],

      // 分页及排序
      page: 1,
      page_size: 10,
      total_page: 0,

      // 加载过渡状态
      loading: false,

      // 防止过渡加载变量
      load: true,

      // 订单号
      order_id: ""
    };
  },
  mounted() {
    if (this.$route.params.id) {
      // 判断一下再赋值，防止被赋undefined
      this.order_id = this.$route.params.id;
    }
    this.query_order();
  },
  methods: {
    // 获取订单列表
    get_orders() {
      this.$api
        .orders({
          page: this.page,
          page_size: this.page_size
        })
        .then(res => {
          this.orders = res.data.results;
          //   向上取整拿到总页数
          this.total_page = Math.ceil(res.data.count / this.page_size);

          // scrollHeight: 元素的高度即表格内容的高度
          // scrollTop: 元素滚动出去的高度
          // clientHeight: 元素可视区域的高度
          // 当scrollTop + clientHeight = scrollHeight 时,滚动条滚动到底部
          // 监听表格dom对象的滚动事件
          //   let dom = document.querySelector('.el-table__body');
          let dom = this.$refs.table.bodyWrapper;
          let that = this;
          dom.addEventListener("scroll", function() {
            const scrollDistance =
              dom.scrollHeight - dom.scrollTop - dom.clientHeight;
            // 增加一个判断条件，避免查询单条时触发
            if (scrollDistance <= 0 && that.load) {
              //等于0证明已经到底，可以请求接口
              if (that.page < that.total_page) {
                //当前页数小于总页数就请求
                that.page++; //当前页数自增
                that.loading = true; // 展示加载中过渡状态
                that.load = false;
                //请求接口的代码
                that.$api
                  .orders({
                    page: that.page,
                    page_size: that.page_size
                  })
                  .then(res => {
                    //将请求回来的数据和当前展示的数据合并在一起
                    that.orders = that.orders.concat(res.data.results);
                    that.loading = false;
                    that.load = true;
                  })
                  .catch(() => {
                    that.loading = false;
                    that.load = true;
                  });
              }
            }
          });
        });
    },

    // 查询单条订单
    get_order(order_id) {
      this.loading = true; // 展示加载中过渡状态
      this.load = false;
      this.$api
        .order(order_id)
        .then(res => {
          // 将查询的单条数据push到列表
          this.orders.push(res.data);
          this.loading = false;
          this.load = true;
        })
        .catch(() => {
          this.loading = false;
          this.load = true;
        });
    },

    // 查询订单
    query_order() {
      this.orders = []; // 搜索之前都先清空列表
      this.page = 1; // 重置page为第一页
      if (this.order_id) {
        this.get_order(this.order_id);
      } else {
        this.get_orders();
      }
    },

    // 立即支付
    pay_order(order_id) {
      this.$api.payment_url(order_id).then(res => {
        window.open(res.data.url);
        // location.href = res.data.url;
      });
    }
  }
};
</script>
<style scoped >
.el-divider {
  margin: 0.5em;
  margin-left: 0;
  padding: 0.1em 0;
  background-color: tomato;
}
div /deep/.el-input__inner {
  border: 2px solid #e23b3b;
}
</style>