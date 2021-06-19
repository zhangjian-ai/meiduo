<template>
  <Container>
    <!-- 详情栏 -->
    <el-row class="main">
      <el-col :span="3">
        <pre style="margin:0; padding: 0;">&nbsp;</pre>
      </el-col>
      <!-- 详情导航 -->
      <el-col :span="4">
        <div class="category-detail">
          <el-menu router class="el-menu-vertical-demo" :default-active="active_index">
            <p style="font-size: 1.2em; color: red;">用户中心</p>
            <el-divider></el-divider>
            <el-menu-item index="detail">
              <i class="el-icon-user"></i>
              <span slot="title">个人信息</span>
            </el-menu-item>
            <el-menu-item index="orders">
              <i class="el-icon-tickets"></i>
              <span slot="title">全部订单</span>
            </el-menu-item>
            <el-menu-item index="address">
              <i class="el-icon-location-information"></i>
              <span slot="title">收货地址</span>
            </el-menu-item>
            <el-menu-item>
              <i class="el-icon-unlock"></i>
              <span slot="title">修改密码</span>
            </el-menu-item>
          </el-menu>
        </div>
      </el-col>
      <!-- 详情展示区 -->
      <el-col :span="14">
          <router-view></router-view>
      </el-col>
    </el-row>
    <!-- 页脚 -->
    <Footer></Footer>
  </Container>
</template>
<script>
import Footer from "@/components/Footer.vue";
import Container from "@/components/Container.vue";

export default {
  name: "UserCenter",
  data() {
    return {
      // 当前激活菜单
      active_index: ""
    };
  },
  methods: {},
  mounted() {
    // 菜单栏默认选中
    var url = window.location.href;
    if (url.includes("detail")) {
      this.active_index = "detail";
      return;
    }
    if (url.includes("address")) {
      this.active_index = "address";
      return;
    }
    if (url.includes("orders")) {
      this.active_index = "orders";
      return;
    }
    if (url.includes("setpwd")) {
      this.active_index = "setpwd";
      return;
    }
  },
  components: {
    Footer,
    Container
  }
};
</script>
<style scoped>
.main {
  height: 33em;
}

.category-detail {
  width: 12em;
  height: 32em;
  background-color: rgb(207, 210, 218);
  text-align: center;
  border-radius: 3px;
}
.category-detail .el-menu {
  background-color: inherit;
  border-radius: inherit;
}

.el-divider {
  margin: 0;
  margin-right: 1em;
  padding: 0;
}
</style>