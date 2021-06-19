<template>
  <Container>
    <Category></Category>
    <div class="main">
      <!-- 商品信息 -->
      <el-row>
        <el-col :span="3">
          <pre style="margin:0; padding: 0;">&nbsp;</pre>
        </el-col>
        <el-col :span="16">
          <div style="min-height: 30em; width: 70em;">
            <el-col :span="4" v-for="item in sku_set" :key="item.text" class="detail_box">
              <span class="stock">剩余{{ item.object.stock }}件</span>
              <el-link
                :underline="false"
                @click="$router.push({name: 'sku_detail', query:{sku_id: item.object.id}})"
              >
                <el-image :src="item.object.default_image_url"></el-image>
              </el-link>
              <div class="text" :title="item.object.name">{{ item.object.name }}</div>
              <div style="color:red;">
                {{ item.object.price }}
                <span class="comments">{{ item.object.comments }}条评价</span>
              </div>
            </el-col>
          </div>
        </el-col>
      </el-row>
      <!-- 分页 -->
      <el-row>
        <div style="text-align: center;">
          <el-pagination
            background
            @current-change="handleCurrentChange"
            :page-size="page_size"
            :current-page="page"
            layout="prev, pager, next"
            :total="total"
          ></el-pagination>
        </div>
      </el-row>
    </div>
  </Container>
</template>
<script>
/* eslint-disable */

import Container from "@/components/Container.vue";
import Category from "@/components/Category.vue";

export default {
  data() {
    return {
      // 搜索栏传入的text
      text: "",
      //   分页变量
      page: 1,
      page_size: 12,
      total: 0,

      // 查询结果
      sku_set: []
    };
  },
  mounted() {
    this.text = this.$route.query.text;
    // this.text = this.$route.params.text;

    this.get_goods();
  },
  methods: {
    // 这是分页函数
    handleCurrentChange(currentPage) {
      this.page = currentPage;
      //   每次页码切换后就掉一次查询
      this.get_goods();
    },

    // 查询sku
    get_goods() {
      this.$api
        .search({
          page: this.page,
          page_size: this.page_size,
          text: this.text
        })
        .then(res => {
          //   后端处理分页
          this.sku_set = res.data.results;
          this.total = res.data.count;
        });
    }
  },
  watch: {
    // 监听路由变化，解决同一url不同参数时，页面不刷新的问题
    $route(to, from) {
        if (to.query.text != from.query.text) {
          this.text = to.query.text;
          this.get_goods(); // 重新加载数据
        }
    }
  },
  components: {
    Container,
    Category
  }
};
</script>
<style scoped>
.main {
  margin-top: 2em;
}
.main .el-row {
  margin-top: 1em;
  margin-bottom: 0;
}
.detail_box {
  width: 10em;
  margin: 0.75em 0.5em;
  padding: 0.5em 0.5em;
}

.text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 0.5em;
  color: grey;
}
.stock {
  position: absolute;
  z-index: 8;
  font-size: 0.5em;
  color: rgb(133, 131, 131);
  background-color: rgb(217, 224, 224);
}
.comments {
  margin-left: 2em;
  font-size: 0.5em;
  color: grey;
}
</style>