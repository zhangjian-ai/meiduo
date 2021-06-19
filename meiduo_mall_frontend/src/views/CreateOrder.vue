<template>
  <Container>
    <el-row>
      <el-col :span="3">
        <pre style="margin:0; padding: 0;">&nbsp;</pre>
      </el-col>
      <el-col :span="18">
        <!-- 收货地址 -->
        <el-row>
          <p class="row_title">
            <span>收货地址</span>
          </p>
          <el-divider></el-divider>
          <div class="text_box">
            <div class="address">
              <el-radio-group v-model="address_id">
                <el-radio
                  v-for="address in addresses"
                  :key="address.id"
                  :label="address.id"
                  style="margin-top:0.5em;"
                >
                  {{ address.province }}&nbsp;{{address.city}}&nbsp;{{address.district}}&nbsp;{{address.place}}
                  &nbsp;（{{address.receiver}}&nbsp;收）{{address.mobile}}
                </el-radio>
              </el-radio-group>
            </div>
          </div>
        </el-row>
        <!-- 支付方式 -->
        <el-row>
          <p class="row_title">
            <span>支付方式</span>
          </p>
          <el-divider></el-divider>
          <div class="text_box">
            <div class="address">
              <el-radio-group v-model="pay_method">
                <el-radio :label="1" style="margin:0 0.5em;">货到付款</el-radio>
                <el-radio :label="2" style="margin:0 0.5em;">支付宝</el-radio>
                <el-radio :label="3" style="margin:0 0.5em;">微信</el-radio>
              </el-radio-group>
            </div>
          </div>
        </el-row>
        <!-- 商品列表 -->
        <el-row>
          <p class="row_title">
            <span>商品列表</span>
          </p>
          <el-divider></el-divider>
          <div>
            <div>
              <el-table
                :data="skus"
                size="mini"
                height="32em"
                :header-cell-style="{background:'#eef1f6',color:'#606266', 'text-align': 'center'}"
                :header-row-style="{height:'3em'}"
              >
                <el-table-column type="index" width="40" align="center"></el-table-column>
                <el-table-column width="150" align="center">
                  <template slot-scope="scope">
                    <el-image :src="scope.row.default_image_url" style="width: 8em; height: 8em;"></el-image>
                  </template>
                </el-table-column>
                <el-table-column prop="name" label="商品名称" width="300"></el-table-column>
                <el-table-column prop="spec" label="规格" width="200" align="center"></el-table-column>
                <el-table-column prop="price" label="价格" width="120" align="center"></el-table-column>
                <el-table-column label="数量" width="90" align="center">
                  <template slot-scope="scope">{{ scope.row.count }}</template>
                </el-table-column>
                <el-table-column label="小计" width="150" align="center">
                  <template
                    slot-scope="scope"
                  >{{ (scope.row.count * scope.row.price).toFixed(2) }} &nbsp;元</template>
                </el-table-column>
              </el-table>
            </div>
          </div>
        </el-row>
        <!-- 提交订单 -->
        <el-row>
          <p class="row_title">
            <span>提交订单</span>
          </p>
          <el-divider></el-divider>
          <div class="text_box">
            <p class="settle">
              <span style="font-size: 0.5em;">共：</span>
              <span style="font-size: 1em; color: red;">&nbsp;{{ settle.count }}&nbsp;</span>
              <span style="font-size: 0.5em;">件商品，&nbsp;</span>
              <span style="font-size: 0.5em;">总金额：</span>
              <span style="font-size: 1em; color: red;">{{ settle.goods_price.toFixed(2) }}&nbsp;元</span>
            </p>
            <p class="settle">
              <span style="font-size: 0.5em;">运费：</span>
              <span style="font-size: 1em; color: red;">&nbsp;{{ settle.freight.toFixed(2) }}&nbsp;元</span>
            </p>
            <p class="settle">
              <span style="font-size: 0.5em;">实付款：</span>
              <span
                style="font-size: 1em; color: red;"
              >&nbsp;{{ settle.total_amount.toFixed(2) }}&nbsp;元</span>
            </p>
          </div>
          <div>
            <el-col :span="20">
              <pre style="margin:0; padding: 0;">&nbsp;</pre>
            </el-col>
            <el-col :span="4">
              <div class="submit_button">
                <el-link
                  style="color: white; font-size: 1.2em;"
                  :underline="false"
                  @click="submit_order"
                >提&nbsp;交&nbsp;订&nbsp;单</el-link>
              </div>
            </el-col>
          </div>
        </el-row>
        <!-- 创建订单成功后的弹框 -->
        <el-dialog :visible.sync="dialogVisible" width="40em" :before-close="handleClose">
          <el-row>
            <el-col :span="6">
              <el-image :src="success" style="width: 10em;"></el-image>
            </el-col>
            <el-col :span="18" style="text-align: center;">
              <p class="create_success">
                <span>恭喜！订单创建成功，订单号：</span>
                <span style="color: red;">{{ order_id }}</span>
              </p>
              <p class="create_success">
                <span>感谢您在张老师的平台购物，祝您购物愉快！</span>
              </p>
              <p class="create_success">
                <span>如有任何问题，请联系张老师当面解决。其他任何途径一概不理，就这么银杏！</span>
              </p>
            </el-col>
          </el-row>
          <span slot="footer" class="dialog-footer">
            <el-button @click="$router.replace({name: 'home'})">继 续 购 物</el-button>
            <el-button v-if="pay_method != 1" type="danger" @click="pay_order">立 即 支 付</el-button>
          </span>
        </el-dialog>
      </el-col>
    </el-row>
  </Container>
</template>
<script>
import Container from "@/components/Container.vue";

export default {
  name: "CreateOrder",
  data() {
    return {
      // 需要生成订单的sku数组
      skus: [],

      // 收货地址、当前选中的收货地址
      addresses: [],
      address_id: 0,

      // 支付方式
      pay_method: 2,

      // 创建成功的订单号
      order_id: 0,

      // 创建订单后的弹窗展示变量
      dialogVisible: false,

      // 本地图片
      success: require("../assets/images/success.jpeg")
    };
  },
  mounted() {
    this.get_addrsss();
    this.order_list();
  },
  methods: {
    // 获取收货地址
    get_addrsss() {
      this.$api.address().then(res => {
        this.addresses = res.data.address;
        this.address_id = this.addresses[0].id;
      });
    },
    // 待结算商品列表
    order_list() {
      this.$api.order_settlement_list().then(res => {
        this.skus = res.data;
      });
    },

    // 提交订单
    submit_order() {
      // 准备数据
      let data = {
        address: this.address_id,
        pay_method: this.pay_method,
        total_count: this.settle.count,
        total_amount: this.settle.total_amount,
        freight: this.settle.freight
      };
      this.$api.submit_order(data).then(res => {
        if (res.status == 201) {
          this.order_id = res.data.order_id;
          this.dialogVisible = true;
        }
      });
    },

    // 立即支付
    pay_order() {
      if (this.pay_method == 2) {
        this.$api.payment_url(this.order_id).then(res => {
          window.open(res.data.url);
          // location.href = res.data.url;
          this.$router.push({ name: "orders", params: { id: this.order_id } });
        });
      }
      if (this.pay_method == 3) {
        this.$message({
          message: "暂不支持微信支付！",
          type: "warning"
        });
      }
    },

    // 离开支付的确认弹窗
    handleClose() {
      if (this.pay_method != 1) {
        this.$confirm("当前订单还未支付，确认离开？").then(() => {
          this.$router.replace({ name: "cart" });
        });
      }
    }
  },
  computed: {
    // 计算商品数量、运费、总金额等
    settle() {
      let count = 0;
      let goods_price = 0;
      this.skus.forEach(sku => {
        count += sku.count;
        goods_price += sku.count * sku.price;
      });
      let freight = (10 * count) / 2;
      return {
        count: count,
        goods_price: goods_price,
        freight: freight,
        total_amount: freight + goods_price
      };
    }
  },
  components: {
    Container
  }
};
</script>
<style  scoped>
.el-row {
  margin-bottom: 2em;
}
.el-divider {
  margin: 0;
  padding: 0.1em 0;
  background-color: tomato;
}
.row_title {
  margin: 0;
  padding: 0;
  font-size: 1.2em;
}
.text_box {
  background-color: #eef1f6;
}
.address {
  padding: 1em;
  padding-left: 1em;
  width: 70%;
}
.settle {
  margin: 0 0;
  padding: 0.2em 1em;
  text-align: right;
}
.submit_button {
  background-color: rgb(236, 62, 62);
  margin-top: 1em;
  height: 3em;
  line-height: 3em;
  text-align: center;
}
.create_success {
  margin: 0 0;
  padding: 0.2em 1em;
  text-align: left;
}
</style>