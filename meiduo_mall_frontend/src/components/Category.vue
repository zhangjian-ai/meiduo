<template>
  <!-- 商品分类 -->
  <el-row>
    <div>
      <!-- 商品分类栏 -->
      <el-row class="category">
        <el-col :span="2">
          <pre style="margin:0; padding: 0;">&nbsp;</pre>
        </el-col>
        <el-col :span="4" class="pre">
          <div @mouseleave="hiden_category()" style="width: inherit;">
            <div @mouseenter="show_title = true" style="width: 15em;">
              <el-link :underline="false" type="text">商&nbsp;品&nbsp;分&nbsp;类</el-link>
            </div>
            <div class="category-title" v-if="show_title">
              <!-- 频道分类 -->
              <div
                class="title"
                v-for="(item, index) in category"
                :key="index"
                @mouseenter="show_category_detail(index)"
              >
                <el-link
                  type="primary"
                  :underline="false"
                  v-for="channel in item.channels"
                  :key="channel.url"
                  :href="channel.url"
                >{{ channel.category }}</el-link>
              </div>
              <!-- 详细分类 -->
              <div class="category-detail" v-if="show_detail">
                <p v-for="(item, index) in category_detail" :key="index">
                  <el-link :underline="false">
                    {{ item.name }}
                    <i class="el-icon-d-arrow-right el-icon--right"></i>
                  </el-link>
                  <el-link
                    type="primary"
                    v-for="channel in item.sub_cats"
                    @click="$router.push({name: 'skus', query:{category_id: channel.id}})"
                    :key="channel.name"
                  >{{ channel.name }}</el-link>
                </p>
              </div>
            </div>
          </div>
        </el-col>
        <el-col :span="12">
          <div style="text-align: left; margin-left:5em;">
            <el-link :underline="false">&nbsp;首页&nbsp;</el-link>
            <el-divider direction="vertical"></el-divider>
            <el-link :underline="false">&nbsp;真划算&nbsp;</el-link>
            <el-divider direction="vertical"></el-divider>
            <el-link :underline="false">&nbsp;抽奖&nbsp;</el-link>
          </div>
        </el-col>
      </el-row>
    </div>
  </el-row>
</template>
<script>
export default {
  name: "Category",
  data() {
    return {
      // 展示分类详情布尔值及内容
      show_title: false,
      show_detail: false,
      category: [],
      category_detail: []
    };
  },
  mounted() {
    this.get_category_channel();
  },
  methods: {
    // 获取商品频道级分类信息
    get_category_channel() {
      let that = this;
      that.$axios
        .get("goods_channel/")
        .then(res => {
          that.category = res.data.data;
        })
    },
    // 展示频道详细分类
    show_category_detail(index) {
      this.category_detail = this.category[index].sub_cats;
      this.show_detail = true;
    },

    // 隐藏频道及分类信息
    hiden_category() {
      this.show_title = false;
      this.show_detail = false;
    }
  }
};
</script>
<style scoped>
.category {
  background-color: rgb(206, 205, 202);
  text-align: center;
}
.pre {
  background-color: rgb(177, 171, 171);
}
.category-title {
  position: absolute;
  z-index: 10;
  width: inherit;
  height: 18.8em;
  background-color: rgb(233, 230, 230);
}

.category-title .title {
  font-family: Hiragino Sans GB;
  height: 1.5em;
  line-height: 1.5em;
  text-align: left;
  padding-left: 1em;
}
.category-title div:hover {
  background-color: rgb(251, 253, 253);
}
.title .el-link {
  margin: 0 0.5em;
  color: rgb(20, 19, 19);
}
.category-detail {
  position: absolute;
  z-index: 10;
  width: 45em;
  height: 18.8em;
  left: 100%;
  bottom: 0;
  background-color: rgb(251, 253, 253);
}
p {
  margin: 0 0;
  height: 1.75em;
  line-height: 1.75em;
  text-align: left;
}
p .el-link {
  margin: 0 0.5em;
  font-family: Hiragino Sans GB;
  font-size: 0.8em;
  padding-left: 0.5em;
}
</style>