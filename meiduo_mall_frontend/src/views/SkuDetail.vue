<template>
  <Container>
    <Category></Category>
    <!-- 详情展示区 -->
    <el-row>
      <el-col :span="2">
        <pre style="margin:0; padding: 0;">&nbsp;</pre>
      </el-col>
      <el-col :span="20">
        <div class="detail">
          <!-- 图片展示 -->
          <el-col :span="8">
            <div class="image">
              <el-image :src="sku_data.default_image_url"></el-image>
            </div>
            <div class="img-list">
              <el-scrollbar>
                <ul>
                  <li v-for="item in sku_data.images" :key="item.image">
                    <el-popover placement="top" trigger="hover">
                      <img :src="item.image" style="height: 30em;width: 30em" />
                      <img
                        slot="reference"
                        :src="item.image"
                        style="max-height: 3em;max-width: 3em"
                      />
                    </el-popover>
                  </li>
                </ul>
              </el-scrollbar>
            </div>
          </el-col>
          <el-col :span="2">
            <pre style="margin:0; padding: 0;">&nbsp;</pre>
          </el-col>
          <!-- 规格详情 -->
          <el-col :span="14">
            <div class="text">
              <div>
                <p style="font-size: 1.5em;">{{ sku_data.name }}</p>
                <span style="font-size: 0.2em; color: grey;">{{ sku_data.caption }}</span>
              </div>
              <div class="price">
                <p style="height: 4em; line-height:4em;">
                  <span style="font-size: 2em; color:red; margin-left: 0.5em;">{{ sku_data.price }}</span>
                  <span style="font-size: 0.2em; margin-left: 10em;">市场价：{{ sku_data.market_price }}</span>
                  <span
                    style="font-size: 0.2em; margin-left: 60em; color: grey;"
                  >{{ sku_data.comments }} 条评价</span>
                </p>
              </div>
              <div>
                <span>数量：</span>
                <el-input-number v-model="num" :min="1" :max="sku_data.stock" size="mini"></el-input-number>
                <span
                  style="font-size: 0.2em; margin-left: 15em; color: grey;"
                >剩余库存：{{ sku_data.stock }}</span>
              </div>
              <div v-for="(spec, index) in sku_data.specs" :key="spec.name">
                <span>{{ spec.name }}：&nbsp;</span>
                <el-radio-group v-model="choice[index]" size="mini" fill="red">
                  <el-radio-button
                    v-for="value in spec.list"
                    :key="value"
                    :label="value"
                  >{{ value }}</el-radio-button>
                </el-radio-group>
              </div>
              <div>
                <span>总价：¥</span>
                <span style="font-size: 2em; color:red; margin-left: 0.5em;">{{ final_price }}</span>
              </div>
              <div style="margin-top: 2em;">
                <p>
                  <el-button type="danger" @click="buy_now()" :disabled="status">立即购买</el-button>
                  <el-button type="danger" plain @click="add_cart()" :disabled="status">加入购物车</el-button>
                </p>
              </div>
            </div>
          </el-col>
        </div>
      </el-col>
    </el-row>
    <!-- 其他信息：介绍，配件清单，售后 -->
    <el-row>
      <div class="description" v-if="sku_data.desc">
        <div v-html="sku_data.desc.desc_detail" style="text-align: center;"></div>
        <div v-html="sku_data.desc.desc_pack"></div>
        <div v-html="sku_data.desc.desc_service"></div>
      </div>
    </el-row>
  </Container>
</template>
<script>
/* eslint-disable */
import Container from "@/components/Container.vue";
import Category from "@/components/Category.vue";

export default {
  name: "SkuDetail",
  data() {
    return {
      // 查询结果
      sku_data: {},

      // sku_id
      sku_id: 1,

      // 数量
      num: 1,

      // 规格选择数组
      choice: [],

      // 总价
      final_price: 0,

      // 商品库存为0时，失效购买和加入购物车按钮
      status: false
    };
  },
  mounted() {
    this.sku_id = this.$route.query.sku_id;
    this.get_sku_detail();
    this.set_history();
  },
  methods: {
    // 获取sku详情数据
    get_sku_detail() {
      let that = this;
      that.$axios.get("sku_detail/" + that.sku_id + "/").then(res => {
        that.sku_data = res.data;
        that.final_price = that.sku_data.price;
        if (that.sku_data.stock == 0) {
          that.status = true;
        }
      });
    },
    // 添加购物车
    add_cart() {
      if (this.$api.check_spec(this.choice, this.sku_data.specs)) {
        this.$message({
          message: "请先选择商品规格",
          type: "warning",
        });
        return;
      }
      let that = this;
      that.$axios
        .post("cart/", {
          sku_id: that.sku_id,
          count: that.num,
          spec: that.choice.join("_")
        })
        .then(res => {
          that.$notify({
            type: "success",
            title: "添加购物车成功"
          });
        });
    },

    // 立即购买
    buy_now() {
      if (this.$api.check_spec(this.choice, this.sku_data.specs)) {
        this.$message({
          message: "请先选择商品规格",
          type: "warning",
        });
        return;
      }
      if (this.$store.state.token == undefined) {
        this.$notify.warning({
          title: "请先登陆"
        });
        return;
      }
      let that = this;
      that.$axios
        .post("cart/", {
          sku_id: that.sku_id,
          count: that.num,
          spec: that.choice.join("_")
        })
        .then(() => {
          // 准备数据
          let request_data = [];
          request_data[0] = {
            sku_id: that.sku_id,
            spec: that.choice.join("_")
          };
          let params = { skus: request_data };

          that.$api.selects(params).then(res => {
            if (res.status == 201) {
              that.$router.push({
                name: "create_order"
              });
            }
          });
        });
    },

    // 保存浏览记录
    set_history() {
      if (this.$store.state.token) {
        this.$axios.post("set_history/", {
          sku_id: this.sku_id
        });
      }
      return;
    }
  },
  components: {
    Container,
    Category
  },
  watch: {
    num: function() {
      this.final_price = this.sku_data.price * this.num;
    }
  }
};
</script>
<style  scoped>
.detail {
  height: 35em;
}
.image {
  width: 24em;
  height: 24em;
  margin-top: 2em;
  margin-bottom: 2em;
}
.img-list {
  background-color: rgb(199, 193, 193);
  border-radius: 0.5em;
}
ul {
  display: flex;
}
li {
  display: inline-block;
  flex-shrink: 0;
  margin: 0 1em;
  padding: 0 0;
}

.text {
  text-align: left;
  width: 40em;
}

.text div {
  margin: 1em 0;
}

.price {
  background-color: rgb(235, 225, 230);
}

.description {
  width: 80%;
  margin-left: 6em;
  padding: 1em 3em;
  background-color: rgb(131, 157, 179);
  border-radius: 1em;
}
</style>