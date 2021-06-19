<template>
  <div style="width: 50em; margin-top: 2em;">
    <div v-if="loading">
      <el-image :src="image.loading"></el-image>
    </div>
    <div v-if="verify_pass">
      <el-image :src="image.success" style="width: 5em; height: 5em;"></el-image>
      <p style="font-size: 2.5em; color: green;">恭喜您，认证成功！</p>
      <el-button type="primary" @click="$router.push({name: 'home'})">返回主页</el-button>
    </div>
    <div v-if="verify_fail">
      <el-image :src="image.failure" style="width: 5em; height: 5em;"></el-image>
      <p style="font-size: 2.5em; color: red;">认证失败！</p>
      <p style="font-size: 1em; color: red;">失败原因：{{ error_message }}</p>
      <el-button type="primary" @click="$router.push({name: 'home'})">返回主页</el-button>
    </div>
  </div>
</template>
<script>
export default {
  name: "VerifyEmail",
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
      }
    };
  },
  mounted() {
    this.verify_email();
  },
  methods: {
    // 获取回调地址中的字段的值
    getCode(name) {
      let url = window.location.href;

      let params = url.substr(url.lastIndexOf("?") + 1).split("&");
      for (let i = 0; i < params.length; i++) {
        let param = params[i];
        let key = param.split("=")[0];
        let value = param.split("=")[1];
        if (key === name) {
          return value;
        }
      }
    },
    verify_email() {
      let token = this.getCode("token");
      let that = this;
      that.$axios
        .get("verify_email/", {
          params: {
            token: token
          }
        })
        .then(() => {
          that.loading = false;
          that.verify_pass = true;
        })
        .catch(err => {
          that.loading = false;
          that.verify_fail = true;
          that.error_message = err.response.data.msg;
        });
    }
  }
};
</script>
<style scoped>
p {
  margin: 0.5em;
}

div {
  background-color:white;
  text-align: center;
}
</style>