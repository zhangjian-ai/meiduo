<template>
  <el-container>
    <!-- header部分 -->
    <el-header style="height: 15%;">
      <el-col :span="8" class="login_banner">
        <el-image :src="image.logo"></el-image>
      </el-col>
    </el-header>
    <!-- 主体部分 -->
    <el-main>
      <el-col :span="15" class="login_banner">
        <el-image :src="image.login_banner"></el-image>
      </el-col>
      <el-col :span="1" style="margin-top: 6em; text-align: center;">
        <div class="banner-text">
          <span>商品美·种类多·欢迎选购</span>
        </div>
      </el-col>
      <el-col :span="7" class="login_banner">
        <div class="login_container">
          <div class="subs">
            <div class="login-text">用&nbsp;户&nbsp;登&nbsp;陆</div>
            <el-divider></el-divider>
            <!-- --------表单部分-------- -->
            <!-- 钉钉二维码 这里因为不能使用v-if 所以用了两个变量来决定两种登陆方式的展示  v-if 会销毁掉DOM元素 导致无法加载出二维码-->
            <div v-show="show">
              <div id="login"></div>
            </div>
            <!-- 正常登陆表单 -->
            <div v-if="disappear" class="subs-subs">
              <el-form :model="form" :rules="rules" ref="from">
                <el-form-item prop="username">
                  <el-input
                    v-model="form.username"
                    placeholder="请输用户名或手机号"
                    suffix-icon="el-icon-user"
                  ></el-input>
                </el-form-item>
                <el-form-item prop="password">
                  <el-input
                    v-model="form.password"
                    type="password"
                    placeholder="请输入密码"
                    suffix-icon="el-icon-lock"
                  ></el-input>
                </el-form-item>
                <span class="errmsg">{{ msg }}</span>
                <el-form-item class="keep-alive">
                  <el-checkbox v-model="keep" true-label="true">保持登陆</el-checkbox>
                </el-form-item>
                <el-form-item>
                  <el-button type="danger" style="width: 18em;" @click="submit">登&nbsp;陆</el-button>
                </el-form-item>
              </el-form>
            </div>

            <el-divider></el-divider>
            <div>
              <el-row>
                <el-col :span="4">
                  <el-link @click="qq_login" :underline="false" type="primary">QQ登陆</el-link>
                </el-col>
                <el-col :span="6">
                  <el-link @click="dt_login" :underline="false" type="primary">{{ type }}</el-link>
                </el-col>
                <el-col :span="4">
                  <el-link @click="$router.push({name: 'home'})" :underline="false" type="info">游客</el-link>
                </el-col>
                <el-col :span="10">
                  <!-- click事件直接绑定router内置函数完成页面跳转 -->
                  <el-link
                    :underline="false"
                    type="danger"
                    @click="$router.push({ name: 'register', query:{redirect: $route.query.redirect} })"
                  >
                    立即注册
                    <i class="el-icon-d-arrow-right el-icon--right"></i>
                  </el-link>
                </el-col>
              </el-row>
            </div>
          </div>
        </div>
      </el-col>
    </el-main>
    <!-- footer部分 -->
    <Footer style="height: 15%;"></Footer>
  </el-container>
</template>

<script>
/* eslint-disable */ //------由于引入了外部js，此处失效eslint校验
import Footer from "@/components/Footer.vue";

export default {
  name: "Login",
  data() {
    return {
      // 本地图片资源
      image: {
        logo: require("../assets/images/logo02.png"),
        login_banner: require("../assets/images/login_banner.png")
      },

      // 登陆表单
      form: {
        username: "",
        password: ""
      },
      // 表单校验规则
      rules: {
        username: [
          {
            required: true,
            message: "  请填写用户名",
            trigger: "blur"
          }
        ],
        password: [
          {
            required: true,
            message: "  请填写密码",
            trigger: "blur"
          }
        ]
      },

      // 保持登陆
      keep: "",

      //错误信息
      msg: "",

      //展示钉钉登陆二维码
      show: false,
      disappear: true,
      type: "钉钉登陆",

      // 重定向路径
      redirect: ""
    };
  },
  mounted() {},
  methods: {
    // 登陆提交
    submit() {
      this.$refs.from.validate(valid => {
        if (valid) {
          let that = this;

          that.$axios
            .post("login/", that.form)
            .then(res => {
              // 登陆成功后，保存token信息
              sessionStorage.clear(); // sessionStorage关闭浏览器即清除
              localStorage.clear(); // 永久保存

              if (that.keep === "true") {
                localStorage.token = res.data.token;
                localStorage.username = res.data.username;
                localStorage.user_id = res.data.id;
              } else {
                sessionStorage.token = res.data.token;
                sessionStorage.username = res.data.username;
                sessionStorage.user_id = res.data.id;
              }

              that.$store.commit("setStatus", {
                username: res.data.username,
                token: res.data.token
              });
              // 跳转页面。根据跳转过来的页面，登陆成功后，跳转回去；否则进入主页
              that.$router.replace(that.$route.query.redirect || "/");
            })
            .catch(err => {
              if (err.non_field_errors) {
                that.msg = "账号或密码错误";
              }
            });
        }
      });
    },

    // QQ登陆
    qq_login() {
      // 获取页面来源路径，如果没有就默认为主页路径
      // let next = this.$route.params.path || "/";
      let that = this;
      this.$axios
        .get("/oauth/qq/authorization/", {
          params: { next: this.$store.state.path }
        })
        .then(res => {
          location.href = res.data.login_url;
        })
        .catch(err => {
          that.$message({
            type: "error",
            message: "调用QQ三方登陆失败，请稍后重试",
            center: true
          });
        });
    },

    // 钉钉登陆，返回二维码跳转的url
    dt_login() {
      // 获取页面来源路径，如果没有就默认为主页路径
      // let next = this.$route.params.path || "/";
      let that = this;

      if (that.show) {
        that.show = false;
        that.disappear = true;
        that.type = "钉钉登陆";
      } else {
        that.show = true;
        that.disappear = false;
        that.type = "账号密码";

        that.$axios
          .get("/oauth/dt/authorization/")
          .then(res => {
            // 展示二维码
            var obj = DDLogin({
              id: "login", //这里需要你在自己的页面定义一个HTML标签并设置id，例如<div id="login_container"></div>或<span id="login_container"></span>
              goto: encodeURIComponent(res.data.url), //请参考注释里的方式
              style: "border:none;background-color:#FFFFFF;",
              width: "250",
              height: "300"
            });

            // 定义监听扫码事件
            var handleMessage = function(event) {
              var origin = event.origin;
              if (origin == "https://login.dingtalk.com") {
                //判断是否来自ddLogin扫码事件。
                var loginTmpCode = event.data;
                //获取到loginTmpCode后就可以在这里构造跳转链接进行跳转了
                // console.log("loginTmpCode", loginTmpCode);
                that.$axios
                  .get("/oauth/dt/authorization/", {
                    params: { loginTmpCode: loginTmpCode }
                  })
                  .then(res => {
                    location.href = res.data.url;
                  })
                  .catch(err => {
                    that.$message({
                      type: "error",
                      message: "调用钉钉三方登陆失败，请稍后重试",
                      center: true
                    });
                  });
              }
            };

            // 在当前窗口增加监听事件
            if (typeof window.addEventListener != "undefined") {
              window.addEventListener("message", handleMessage, false);
            } else if (typeof window.attachEvent != "undefined") {
              window.attachEvent("onmessage", handleMessage);
            }
          })
      }
    }
  },
  components: {
    Footer
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-container {
  height: 100%;
}
.el-header {
  background-color: white;
}

.el-main {
  background-color: rgb(160, 9, 9);
}

.login_banner {
  margin-top: 3em;
  text-align: right;
}
.banner-text {
  color: white;
  width: 1em;
}
.login-text {
  font-size: 1.5em;
  color: red;
  padding-top: 1em;
}
.el-input {
  width: 18em;
}
.login_container {
  background-color: white;
  width: 22em;
}
.subs {
  text-align: center;
  margin-left: 2em;
  width: 18em;
}
.subs-subs {
  text-align: center;
  margin-left: 1em;
  margin-top: 3em;
  width: 16em;
}
.el-divider--horizontal {
  margin-top: 0.5em;
  margin-bottom: 1em;
}
.keep-alive {
  margin-bottom: 0;
  margin-left: 0.5em;
  text-align: left;
}
.el-row {
  text-align: right;
}
.el-row .el-col {
  margin-bottom: 1em;
}
.el-row .el-button {
  padding-top: 0;
}
.el-link {
  font-size: 0.8em;
}
.errmsg {
  margin: 0 0;
  padding: 0 0;
  font-size: xx-small;
  color: red;
}
</style>