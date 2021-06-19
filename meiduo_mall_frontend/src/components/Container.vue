<template>
  <el-container>
    <!-- header -->
    <el-header style="height: 4%;">
      <el-col :span="6">
        <span>欢迎来到美多商城！</span>
      </el-col>
      <el-col :span="16">
        <span v-if="state">欢迎您：{{ username }}</span>
        <span v-else>
          <el-link
            :underline="false"
            @click="$router.replace({name: 'register', query: { redirect: $route.path }})"
          >注册</el-link>
          <el-divider direction="vertical"></el-divider>
          <el-link
            :underline="false"
            @click="$router.replace({name: 'login', query: { redirect: $route.path }})"
          >登陆</el-link>
        </span>
        <el-divider direction="vertical"></el-divider>
        <el-link
          :underline="false"
          @click="$router.push({name: 'orders'})"
          style="color: green;"
          icon="el-icon-s-order"
        >我的订单</el-link>
        <el-divider direction="vertical"></el-divider>
        <el-link
          :underline="false"
          @click="$router.push({name: 'cart'})"
          style="color: red;"
          icon="el-icon-shopping-cart-full"
        >&nbsp;购物车</el-link>
        <el-divider direction="vertical"></el-divider>
        <el-link :underline="false" @click="$router.push({name: 'detail'})" icon="el-icon-user">用户中心</el-link>
        <el-divider direction="vertical"></el-divider>
        <el-link :underline="false" @click="logout" icon="el-icon-switch-button">退出登陆</el-link>
      </el-col>
    </el-header>
    <el-main>
      <Search></Search>
      <!-- 自定义部分 -->
      <slot></slot>
    </el-main>
  </el-container>
</template>

<script>
import Search from "./Search.vue";

export default {
  name: "Container",
  data() {
    return {
      username: "",
      state: false,

      // 当前页面路径
      path: ""
    };
  },
  methods: {
    logout() {
      sessionStorage.clear(); // sessionStorage关闭浏览器即清除
      localStorage.clear(); // 永久保存

      this.$store.commit("setStatus");
      this.$router.push({
        name: "login",
        query: { redirect: this.$route.path }
      });
    }
  },
  components: {
    Search
  },
  mounted() {
    //

    // 获取账号信息
    if (this.$store.state.username) {
      this.username = this.$store.state.username;
      this.state = true;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-main {
  height: 100%;
}
.el-container {
  height: 100%;
}
.el-header {
  background-color: rgb(166, 192, 240);
}
.el-header .el-col {
  text-align: right;
  line-height: 2em;
}
</style>
