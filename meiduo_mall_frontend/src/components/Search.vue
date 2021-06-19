<template>
  <!-- 搜索栏 -->
  <el-row class="banner">
    <el-col :span="6">
      <el-image :src="logo" @click="$router.replace({name: 'home'})"></el-image>
    </el-col>
    <el-col :span="11">
      <el-input placeholder="搜索商品" size="mini" class="input-with-select" v-model="text">
        <el-button slot="append" icon="el-icon-search" @click="go()"></el-button>
      </el-input>
    </el-col>
  </el-row>
</template>
<script>
export default {
  name: "Search",
  data() {
    return {
      // 前端静态图片地址
      logo: require("../assets/images/logo.png"),

      // 搜索框text文本
      text: ""
    };
  },
  methods: {
    go() {
      this.$router.push({ name: "goods_list", query: { text: this.text } });
      // this.$router.push({ name: "goods_list", params: { text: this.text } });
    }
  }
};
</script>
<style scoped>
.banner {
  height: 6em;
}
.banner .el-col {
  text-align: right;
}
.el-input {
  width: 75%;
  margin-top: 2em;
  border: 2px solid red;
  border-radius: 7px;
}
.el-input .el-button {
  color: red;
  font-size: 1.5em;
}

</style>