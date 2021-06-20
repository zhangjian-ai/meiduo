<template>
  <Container>
    <Category></Category>
    <div class="main">
      <!-- 面包屑 -->
      <el-row>
        <el-col :span="2">
          <pre style="margin:0; padding: 0;">&nbsp;</pre>
        </el-col>
        <el-col :span="4">
          <el-breadcrumb style="font-size: 0.5em; color:red;">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>商品列表</el-breadcrumb-item>
          </el-breadcrumb>
        </el-col>
      </el-row>
      <!-- sku信息 -->
      <el-row>
        <el-col :span="2">
          <pre style="margin:0; padding: 0;">&nbsp;</pre>
        </el-col>
        <el-col :span="4">
          <div class="hot">
            <p class="hot_title">热销排行</p>
            <div :span="4" v-for="item in top_set" :key="item" class="hot_detail_box">
              <span class="stock">剩余{{ item.comments }}件</span>
              <el-link
                :underline="false"
                @click="$router.push({name: 'sku_detail', query:{sku_id: item.id}})"
              >
                <el-image :src="item.default_image_url" :alt="item.caption"></el-image>
              </el-link>
              <div class="text" :title="item.name">{{ item.name }}</div>
              <div style="color:red;">{{ item.price }}</div>
            </div>
          </div>
        </el-col>
        <el-col :span="16">
          <div>
            <el-tabs type="card" @tab-click="handleClick">
              <el-tab-pane label="默认"></el-tab-pane>
              <el-tab-pane label="价格"></el-tab-pane>
              <el-tab-pane label="人气"></el-tab-pane>
            </el-tabs>
          </div>
          <div style="min-height: 20em; width: 58em;">
            <el-col :span="4" v-for="item in sku_set" :key="item" class="detail_box">
              <span class="stock">剩余{{ item.stock }}件</span>
              <el-link
                :underline="false"
                @click="$router.push({name: 'sku_detail', query:{sku_id: item.id}})"
              >
                <el-image :src="item.default_image_url"></el-image>
              </el-link>
              <div class="text" :title="item.name">{{ item.name }}</div>
              <div style="color:red;">
                {{ item.price }}
                <span class="comments">{{ item.comments }}条评价</span>
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
  name: "Skus",
  data() {
    return {
      // 上一页面传入sku的分类id
      category_id: 0,
      //   分页变量
      page: 1,
      page_size: 10,
      total: 0,

      // 查询结果
      sku_set: [],
      top_set: [],

      //   排序
      ordering: ["-create_time", "price", "-sales"],
      order: "-create_time"
    };
  },
  mounted() {
    if (this.$route.query.category_id) {
      this.category_id = this.$route.query.category_id;
      this.get_sku();
      this.get_top_sku();
    }else{
      this.$router.replace({name: 'home'})
    }
  },
  methods: {
    // 这是分页函数
    handleCurrentChange(currentPage) {
      this.page = currentPage;
      //   每次页码切换后就掉一次查询
      this.get_sku();
    },
    // 标签页的钩子函数
    handleClick(tab, event) {
      this.order = this.ordering[tab.index];
      this.page = 1;
      this.get_sku();
    },

    // 查询sku
    get_sku() {
      let that = this;
      that.$axios
        .get("sku_list/" + that.category_id + "/skus/", {
          params: {
            page: that.page,
            page_size: that.page_size,
            ordering: that.order
          }
        })
        .then(res => {
          // 后端处理分页
          that.sku_set = res.data.results;
          that.total = res.data.count;
        });
    },

    // 获取热销产品
    get_top_sku() {
      let that = this;
      that.$axios.get("sku_list/" + that.category_id + "/tops/").then(res => {
        that.top_set = res.data;
      });
    }
  },
  watch: {
    // 监听路由变化，解决同一url不同参数时，页面不刷新的问题
    $route(to, from) {
      if (to.query.category_id != from.query.category_id) {
        this.category_id = to.query.category_id;
        this.get_sku();
        this.get_top_sku();
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
  margin-top: 1em;
}
.main .el-row {
  margin-top: 1em;
  margin-bottom: 0;
}
.hot {
  padding-bottom: 0.5em;
  text-align: center;
  background-color: rgb(166, 240, 182);
}
.hot_title {
  margin: 0;
  height: 2em;
  line-height: 2em;
  font-size: 1.2em;
  background-color: hotpink;
}
.hot_detail_box {
  margin: 0.5em;
  margin-left: 2.1em;
  background-color: rgb(19, 236, 229);
  width: 10em;
  text-align: left;
}
.detail_box {
  width: 10em;
  margin: 0.5em 0.75em;
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