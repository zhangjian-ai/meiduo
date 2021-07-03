<template>
  <Container>
    <Category></Category>
    <!-- 广告区域 -->
    <el-row>
      <!-- 轮播图 -->
      <el-row>
        <el-carousel trigger="click">
          <el-carousel-item v-for="item in index_lbt.contents" :key="item.url">
            <el-link :underline="false" :href="item.url" target="_blank">
              <el-image :src="item.image" ></el-image>
            </el-link>
          </el-carousel-item>
        </el-carousel>
      </el-row>
      <!-- 快讯 -->
      <el-row>
        <el-col :span="18">
          <pre style="margin:0; padding: 0;">&nbsp;</pre>
        </el-col>
        <el-col :span="4">
          <div class="index_kx">
            <el-row>
              <p>
                <span style="margin-left:1em;">快讯</span>
                <el-link style="font-size: 0.6em; margin-left:11em;">
                  更多
                  <i class="el-icon-d-arrow-right el-icon--right"></i>
                </el-link>
              </p>
            </el-row>
            <div>
              <p v-for="item in index_kx.contents" :key="item.url">
                <el-link :underline="false" :href="item.url">{{ item.title }}</el-link>
              </p>
            </div>
            <div style="text-align: center;">
              <el-link :underline="false" :href="index_ytgg.url" target="_blank">
                <el-image :src="index_ytgg.image" style="width:inherit; height: 5em;"></el-image>
              </el-link>
            </div>
          </div>
        </el-col>
      </el-row>
      <!-- 1f 手机通讯 -->
      <el-row>
        <el-col :span="2">
          <pre style="margin:0; padding: 0;">&nbsp;</pre>
        </el-col>
        <el-col :span="4">
          <div>
            <p style="font-size: 1.5em;">1F 手机通讯</p>
            <div>
              <el-link :underline="false" :href="index_1f_logo.url" target="_blank">
                <el-image :src="index_1f_logo.image"></el-image>
              </el-link>
            </div>
          </div>
        </el-col>
        <el-col :span="16">
          <el-tabs>
            <el-tab-pane label="时尚新品">
              <div style="height: 30em; overflow:auto; width: 58em;">
                <el-col :span="4" v-for="item in index_1f_ssxp" :key="item.url" class="detail_box">
                  <el-link :underline="false" :href="item.url" target="_blank">
                    <el-image :src="item.image"></el-image>
                  </el-link>
                  <p class="text">{{ item.title }}</p>
                  <p style="color:red;">{{ item.text }}</p>
                </el-col>
              </div>
            </el-tab-pane>
            <el-tab-pane label="畅享低价">
              <div style="height: 30em; overflow:auto; width: 58em;">
                <el-col :span="4" v-for="item in index_1f_cxdj" :key="item.url" class="detail_box">
                  <el-link :underline="false" :href="item.url" target="_blank">
                    <el-image :src="item.image"></el-image>
                  </el-link>
                  <p class="text">{{ item.title }}</p>
                  <p style="color:red;">{{ item.text }}</p>
                </el-col>
              </div>
            </el-tab-pane>
            <el-tab-pane label="手机配件">
              <div style="height: 30em; overflow:auto; width: 58em;">
                <el-col :span="4" v-for="item in index_1f_sjpj" :key="item.url" class="detail_box">
                  <el-link :underline="false" :href="item.url" target="_blank">
                    <el-image :src="item.image"></el-image>
                  </el-link>
                  <p class="text">{{ item.title }}</p>
                  <p style="color:red;">{{ item.text }}</p>
                </el-col>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-col>
      </el-row>
      <!-- 2f 电脑数码 -->
      <el-row>
        <el-col :span="2">
          <pre style="margin:0; padding: 0;">&nbsp;</pre>
        </el-col>
        <el-col :span="4">
          <div>
            <p style="font-size: 1.5em;">2F 电脑数码</p>
            <div>
              <el-link :underline="false" :href="index_2f_logo.url" target="_blank">
                <el-image :src="index_2f_logo.image"></el-image>
              </el-link>
            </div>
          </div>
        </el-col>
        <el-col :span="16">
          <el-tabs>
            <el-tab-pane label="加价换购">
              <div style="height: 30em; overflow:auto; width: 58em;">
                <el-col :span="4" v-for="item in index_2f_jjhg" :key="item.url" class="detail_box">
                  <el-link :underline="false" :href="item.url" target="_blank">
                    <el-image :src="item.image"></el-image>
                  </el-link>
                  <p class="text">{{ item.title }}</p>
                  <p style="color:red;">{{ item.text }}</p>
                </el-col>
              </div>
            </el-tab-pane>
            <el-tab-pane label="畅享低价">
              <div style="height: 30em; overflow:auto; width: 58em;">
                <el-col :span="4" v-for="item in index_2f_cxdj" :key="item.url" class="detail_box">
                  <el-link :underline="false" :href="item.url" target="_blank">
                    <el-image :src="item.image"></el-image>
                  </el-link>
                  <p class="text">{{ item.title }}</p>
                  <p style="color:red;">{{ item.text }}</p>
                </el-col>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-col>
      </el-row>
      <!-- 3f 生活家居 -->
      <el-row>
        <el-col :span="2">
          <pre style="margin:0; padding: 0;">&nbsp;</pre>
        </el-col>
        <el-col :span="4">
          <div>
            <p style="font-size: 1.5em;">3F 生活家居</p>
            <div>
              <el-link :underline="false" :href="index_3f_logo.url" target="_blank">
                <el-image :src="index_3f_logo.image"></el-image>
              </el-link>
            </div>
          </div>
        </el-col>
        <el-col :span="16">
          <el-tabs>
            <el-tab-pane label="生活用品">
              <div style="height: 30em; overflow:auto; width: 58em;">
                <el-col :span="4" v-for="item in index_3f_shyp" :key="item.url" class="detail_box">
                  <el-link :underline="false" :href="item.url" target="_blank">
                    <el-image :src="item.image"></el-image>
                  </el-link>
                  <p class="text">{{ item.title }}</p>
                  <p style="color:red;">{{ item.text }}</p>
                </el-col>
              </div>
            </el-tab-pane>
            <el-tab-pane label="厨房用品">
              <div style="height: 30em; overflow:auto; width: 58em;">
                <el-col :span="4" v-for="item in index_3f_cfyp" :key="item.url" class="detail_box">
                  <el-link :underline="false" :href="item.url" target="_blank">
                    <el-image :src="item.image"></el-image>
                  </el-link>
                  <p class="text">{{ item.title }}</p>
                  <p style="color:red;">{{ item.text }}</p>
                </el-col>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-col>
      </el-row>
    </el-row>
  </Container>
</template>

<script>
import Container from "@/components/Container.vue";
import Category from "@/components/Category.vue";


export default {
  name: "Home",
  props: [],
  data() {
    return {
      // 展示广告相关变量
      contents: [],
      index_lbt: {}, //轮播图
      index_kx: {}, //快讯
      index_ytgg: {}, // 页头广告
      index_1f_logo: {}, // 1f logo
      index_1f_ssxp: {}, // 1f ssxp
      index_1f_cxdj: {}, // 1f cxdj
      index_1f_sjpj: {}, // 1f sjpj

      index_2f_logo: {}, // 2f logo
      index_2f_jjhg: {}, // 2f jjhg
      index_2f_cxdj: {}, // 2f cxdj

      index_3f_logo: {}, // 3f logo
      index_3f_shyp: {}, // 3f shyp
      index_3f_cfyp: {} // 3f cfyp
    };
  },
  mounted() {
    this.get_contents();
  },
  methods: {
    
    // 获取页面广告内容
    get_contents() {
      let that = this;
      that.$axios
        .get("contents/")
        .then(res => {
          that.contents = res.data.data;

          // 给各部分广告分别赋值
          that.index_lbt = that.contents[0];
          that.index_kx = that.contents[1];
          that.index_ytgg = that.contents[2].contents[0];
          that.index_1f_logo = that.contents[3].contents[0];
          that.index_1f_ssxp = that.contents[6].contents;
          that.index_1f_cxdj = that.contents[7].contents;
          that.index_1f_sjpj = that.contents[8].contents;

          that.index_2f_logo = that.contents[9].contents[0];
          that.index_2f_jjhg = that.contents[12].contents;
          that.index_2f_cxdj = that.contents[13].contents;

          that.index_3f_logo = that.contents[14].contents[0];
          that.index_3f_shyp = that.contents[17].contents;
          that.index_3f_cfyp = that.contents[18].contents;
        })
    }
  },
  components: {
    Container,
    Category
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
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

.index_kx {
  position: absolute;
  z-index: 10;
  width: inherit;
  height: 18.8em;
  bottom: 0.85em;
  background-color: rgb(209, 194, 194);
}
.detail_box {
  width: 10em;
  text-align: center;
  margin: 0.5em 0.75em;
  padding: 0.5em 0.5em;
}
.detail_box .text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 0.5em;
  color: grey;
}

/* ---- */
</style>
