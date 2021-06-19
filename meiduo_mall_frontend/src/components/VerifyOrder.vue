<template>
  <div class="main">
    <div v-if="loading">
      <el-image :src="image.loading"></el-image>
    </div>
    <div v-if="verify_pass">
      <div class="display">
        <el-col :span="6">
          <el-image :src="image.success" style="width: 8em;"></el-image>
        </el-col>
        <el-col :span="18" style="text-align: center;">
          <p class="create_success">
            <span>恭喜，支付成功!</span>
          </p>
          <p class="create_success">
            <span>订单号：</span>
            <span style="color: red;">{{ order_id }}</span>
          </p>
          <p class="create_success">
            <span>支付流水号：</span>
            <span style="color: red;">{{ trade_id }}</span>
          </p>
          <p class="create_success">
            <el-button
              type="danger"
              size="mini"
              style="margin-left:15em;"
              @click="$router.push({ name: 'orders', params: { id: order_id } })"
            >查看订单</el-button>
            <el-button type="danger" size="mini" @click="$router.push({name: 'home'})">返回主页</el-button>
          </p>
        </el-col>
      </div>
    </div>
    <div v-if="verify_fail">
      <div class="display">
        <el-col :span="6">
          <p class="create_success">
            <el-image :src="image.failure" style="width: 8em;"></el-image>
          </p>
        </el-col>
        <el-col :span="18" style="text-align: center;">
          <p class="create_success">
            <span>支付出现异常，请联系人工客服处理!</span>
          </p>
          <p class="create_success">
            <span>失败原因：{{ error_message }}</span>
          </p>
          <p class="create_success">
            <el-button
              type="danger"
              size="mini"
              style="margin-left:15em;"
              @click="$router.push({name: 'home'})"
            >返回主页</el-button>
          </p>
        </el-col>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "VerifyOrder",
  data() {
    return {
      // 认证结果
      verify_pass: false,
      verify_fail: false,
      error_message: "",

      // 加载中
      loading: true,

      // 图片路径。引用本地图片时，将图片作为对象导入才能绑定
      image: {
        success: require("../assets/images/success.jpeg"),
        failure: require("../assets/images/failure.jpeg"),
        loading: require("../assets/images/loading.gif")
      },

      // 返回值
      order_id: 0,
      trade_id: 0
    };
  },
  mounted() {
    this.verify_order();
  },
  methods: {
    // 获取回调地址中的参数
    getCode() {
      let url = window.location.href;
      return url.split("?")[1];
    },
    verify_order() {
      let params = this.getCode();
      this.$api
        .verify_alipay(params)
        .then(res => {
          this.loading = false;
          this.verify_pass = true;
          this.order_id = res.data.order_id;
          this.trade_id = res.data.trade_id;
        })
        .catch(err => {
          this.loading = false;
          this.verify_fail = true;
          this.error_message = err.response.data.msg;
        });
    }
  }
};
</script>
<style scoped>
.main {
  text-align: center;
  margin-top: 5em;
}

.create_success {
  margin: 0 0;
  padding: 0 0.2em;
  height: 2em;
  line-height: 2em;
  text-align: left;
}

.el-image {
  margin: 0 0;
  padding: 0 0.2em;
  text-align: right;
}

.display {
  width: 40em;
  height: 8em;
  margin-left: 28em;
  background-color: whitesmoke;
  border-radius: 0.5em;
}
</style>