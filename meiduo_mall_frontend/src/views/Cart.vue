<template>
  <Container>
    <el-divider></el-divider>
    <el-row>
      <el-col :span="2">
        <pre style="margin:0; padding: 0;">&nbsp;</pre>
      </el-col>
      <el-col :span="20">
        <div class="title">
          <p style="font-size: 1.2em; color: red;">
            <span class="el-icon-shopping-cart-full">商品清单</span>
          </p>
        </div>
      </el-col>
    </el-row>
    <!-- 详情展示区 -->
    <el-row>
      <el-col :span="2">
        <pre style="margin:0; padding: 0;">&nbsp;</pre>
      </el-col>
      <el-col :span="20">
        <div class="detail">
          <div>
            <!-- 商品展示 -->
            <el-table
              :data="skus"
              size="mini"
              height="40em"
              highlight-cuurent-row
              ref="skuList"
              :header-cell-style="{background:'#eef1f6',color:'#606266'}"
              :header-row-style="{height:'5em'}"
              @selection-change="handleSelectionChange"
              @row-click="handleRowClick"
            >
              <el-table-column type="selection" align="center"></el-table-column>
              <el-table-column width="150" align="center">
                <template slot-scope="scope">
                  <el-image :src="scope.row.default_image_url" style="width: 8em; height: 8em;"></el-image>
                </template>
              </el-table-column>
              <el-table-column prop="name" label="商品名称" width="300" align="center"></el-table-column>
              <el-table-column prop="spec" label="规格" width="150" align="center"></el-table-column>
              <el-table-column prop="price" label="价格" width="100" align="center"></el-table-column>
              <el-table-column label="数量" width="180" align="center">
                <template slot-scope="scope">
                  <el-input-number
                    v-model="scope.row.count"
                    :min="1"
                    :max="scope.row.stock"
                    size="mini"
                    @change="edit_cart(scope.row)"
                  ></el-input-number>
                </template>
              </el-table-column>
              <el-table-column label="小计" width="120" align="center">
                <!-- 保留两位小数 -->
                <template
                  slot-scope="scope"
                >{{ (scope.row.count * scope.row.price).toFixed(2) }} &nbsp;元</template>
              </el-table-column>
              <el-table-column label="操作" align="center">
                <template slot-scope="scope">
                  <el-button
                    type="danger"
                    icon="el-icon-delete"
                    size="mini"
                    @click="delete_cart(scope.row)"
                  >删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <!-- 结算栏 -->
          <div class="account">
            <el-col :span="15">
              <el-col :span="2">
                <pre style="margin:0; padding: 0;">&nbsp;</pre>
              </el-col>
              <el-col :span="4">
                <p style="font-size: 1.5em;color: red;">结&nbsp;算</p>
              </el-col>
            </el-col>
            <el-col :span="4">
              <p style="text-align: right;">
                <span style="font-size: 0.5em;">合计（不含运费）：</span>
                <span style="font-size: 0.5em; color: red;">¥ &nbsp;</span>
                <span style="font-size: 1.2em; color: red;">{{ total_price }}</span>
              </p>
              <p style="font-size: 0.5em; text-align: right;">
                <span>共计</span>
                <span style="color: red;">&nbsp;{{ count }}&nbsp;</span>
                <span>件商品</span>
              </p>
            </el-col>
            <el-col :span="1">
              <pre style="margin:0; padding: 0;">&nbsp;</pre>
            </el-col>
            <el-col :span="4">
              <div class="submit_button">
                <el-link
                  style="color: white; font-size: 1.2em;"
                  :underline="false"
                  @click="to_create_order"
                >立&nbsp;即&nbsp;付&nbsp;款</el-link>
              </div>
            </el-col>
          </div>
        </div>
      </el-col>
    </el-row>
  </Container>
</template>
<script>
/* eslint-disable */
import Container from "@/components/Container.vue";

export default {
  name: "Cart",
  data() {
    return {
      // 查询结果
      skus: [],

      // 所有商品总价及数量
      total_price: 0,
      count: 0,

      // 选中的sku
      selected_skus: []
    };
  },
  mounted() {
    this.get_cart();
  },
  methods: {
    // 获取购物车信息
    get_cart() {
      let that = this;
      that.$axios.get("cart/").then(res => {
        that.skus = res.data;
      });
    },

    // 勾选事件
    handleSelectionChange(rows) {
      this.count = 0;
      this.total_price = 0;
      this.selected_skus = rows;
      rows.forEach(value => {
        this.total_price += value.count * value.price;
        this.count += value.count;
      });
    },

    // 表格行点击事件，点击行就取消勾选状态并立即再次勾选，为了出发handleSelectionChange
    handleRowClick(row) {
      this.$refs.skuList.toggleRowSelection(row, false);
      // this.$refs.skuList.toggleRowSelection(row, true);
    },

    // 修改购物车信息， 利用async 和 await 实现同步请求
    edit_cart: function(row) {
      // 准备数据
      let request_data = {
        sku_id: row.id,
        count: row.count,
        spec: row.spec
      };

      this.$axios.put("cart/", {
        data: request_data
      });
    },

    // 删除购物车记录
    delete_cart(row) {
      this.$axios
        .delete("cart/", {
          data: row
        })
        .then(res => {
          if (res.status == 200) {
            this.get_cart();
          }
        });
    },

    // 跳转至提交订单页面
    to_create_order() {
      if (this.selected_skus.length == 0) {
        this.$notify.warning({
          title: "请先选择需要购买的商品"
        });
        return;
      }
      if (this.$store.state.token == undefined) {
        this.$notify.warning({
          title: "请先登陆"
        });
        return;
      }

      // 准备数据
      let request_data = [];
      this.selected_skus.forEach((value, index) => {
        let sku = {};
        sku.sku_id = value.id;
        sku.spec = value.spec;

        request_data[index] = sku;
      });
      let params = { skus: request_data };

      this.$api.selects(params).then(res => {
        if (res.status == 201) {
          this.$router.push({
            name: "create_order"
          });
        }
      });
    }
  },
  components: {
    Container
  },
  watch: {}
};
</script>
<style  scoped>
.el-divider {
  margin: 0;
  padding: 0;
  width: 85%;
  margin-left: 6.5em;
}
.el-row {
  margin: 0 0;
}
.detail {
  height: 35em;
  background-color: rgb(248, 219, 156);
}
.submit_button {
  background-color: rgb(236, 62, 62);
  height: 5em;
  line-height: 5em;
  text-align: center;
}
</style>