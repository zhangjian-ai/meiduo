<template>
  <el-footer>
    <el-divider></el-divider>
    <p>
      <el-link type="primary">关于我们</el-link>
      <el-divider direction="vertical"></el-divider>
      <el-link type="primary">联系我们</el-link>
      <el-divider direction="vertical"></el-divider>
      <el-link type="primary">加入我们</el-link>
      <el-divider direction="vertical"></el-divider>
      <el-link type="primary">友情链接</el-link>
    </p>
    <p>CopyRight © 2016 北京美多商业股份有限公司 All Rights Reserved</p>
    <p>电话：010-****888 京ICP备*******8号</p>
  </el-footer>
</template>
<script>
export default {
  name: "Footer"
};
</script>
<style scoped>
.el-footer {
  background-color: white;
  text-align: center;
  font-size: smaller;
}
.el-divider {
  margin: 0;
  padding: 0;
}
.el-link {
  margin: 0.25em 0.5em;
}
</style>