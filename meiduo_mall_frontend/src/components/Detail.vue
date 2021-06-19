<template>
  <!-- 将子页面放在div中，实现滑动效果 -->
  <div style="height: 32em; overflow:auto; width: 50em;">
      <el-row>
        <p style="margin-top: 0;">详情信息</p>
        <el-divider></el-divider>
        <div class="info">
          <el-col :span="1">
            <pre style="margin:0; padding: 0;">&nbsp;</pre>
          </el-col>
          <!-- 用户详情 -->
          <el-col :span="2">
            <p>用户名：</p>
            <p>手机号：</p>
            <p>Email：</p>
          </el-col>
          <el-col :span="14" style="text-align: left;">
            <p>{{ username }}</p>
            <p>{{ mobile }}</p>
            <p>
              <span v-if="has">
                {{ email }}&nbsp;
                <span v-if="email_active">
                  <el-tag type="success" effect="dark" size="mini">已认证</el-tag>
                </span>
                <span v-else>
                  <span style="font-size: 0.5em; color: red;">未收到邮件？</span>
                  <el-button size="mini" type="info" @click="bind_email">重新发送</el-button>
                </span>
              </span>
              <span v-else>
                <span v-if="show">
                  <el-input v-model="input_email" placeholder="请输入邮箱" size="mini"></el-input>&nbsp;
                  <el-button type="primary" @click="bind_email">确认</el-button>
                  <el-button type="info" @click="show = false">取消</el-button>
                </span>
                <span v-else>
                  <span style="font-size: 0.5em; color: red;">当前未绑定邮箱</span>&nbsp;
                  <el-button type="info" @click="show = true">绑定</el-button>
                </span>
              </span>
            </p>
          </el-col>
        </div>
      </el-row>
      <el-row>
        <p>最近浏览</p>
        <el-divider></el-divider>
        <el-col :span="4" v-for="item in sku_set" :key="item.id" class="detail_box">
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
      </el-row>
    </div>
</template>
<script>
/* eslint-disable */
export default {
  name: "Detail",
  data() {
    return {
      // 服务器返回的详细信息
      username: "",
      mobile: "",
      email: "",

      // 认证邮箱逻辑参数
      has: false, // 是否有邮箱
      email_active: false, // 是否已认证
      show: false, // 收否展示邮箱绑定栏

      //绑定邮箱输入框
      input_email: "",

      // 最近浏览记录
      sku_set: []
    };
  },
  mounted() {
    this.get_user_info();
    this.get_browsing_history();
  },
  methods: {
    // 获取用户信息
    get_user_info() {
      let that = this;
      that.$axios.get("user/", {}).then(res => {
        // 加载用户信息
        that.username = res.data.username;
        that.mobile = res.data.mobile;
        if (res.data.email) {
          that.email = res.data.email;
          that.has = true;
          if (res.data.email_active === true) {
            that.email_active = true;
          }
        }
      });
    },

    //绑定邮箱
    bind_email() {
      let that = this;
      if (that.email) {
        that.input_email = that.email;
      }
      // 校验邮箱格式
      let re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
      if (re.test(that.input_email)) {
        //邮箱格式校验通过后，向后端发起请求
        that.$axios
          .put(
            "email/",
            { email: that.input_email },
            {
              // 向后端传递JWT token的方法
              headers: {
                Authorization: "JWT " + that.$store.state.token // 携带token访问接口
              }
            }
          )
          .then(res => {
            // 加载用户信息
            if (that.input_email === res.data.email) {
              that.$notify({
                type: "success",
                title: "邮箱绑定成功",
                message: "请注意查收邮件进行验证，验证邮件有效期为5分钟"
              });
              that.email = res.data.email;
              that.has = true;
            }
          });
      } else {
        that.$notify.error({
          title: "绑定失败",
          message: "邮箱格式错误"
        });
      }
    },

    // 获取最近浏览记录
    get_browsing_history() {
      let that = this;
      that.$axios.get("set_history/").then(res => {
        that.sku_set = res.data;
      });
    }
  }
};
</script>
<style scoped>
.info {
  font-size: 1em;
  height: 8em;
  text-align: right;
  background-color: rgb(243, 240, 240);
  border-radius: 3px;
}
.info .el-button {
  font-size: 1em;
  height: 1.4em;
  padding-top: 0.2em;
  padding-left: 0.3em;
  padding-right: 0.3em;
  margin-left: 0.5em;
}
.info .el-input {
  width: 20em;
  margin-right: 1em;
}
.el-divider {
  margin: 0.5em;
  margin-left: 0;
  padding: 0;
}
.detail_box {
  width: 9em;
  margin: 0.5em 0.5em;
  padding: 0.5em 0.5em;
}

.text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 0.5em;
  color: grey;
}

.comments {
  margin-left: 2em;
  font-size: 0.5em;
  color: grey;
}
</style>