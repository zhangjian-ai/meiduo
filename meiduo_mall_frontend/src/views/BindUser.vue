<template>
  <div>
    <div v-if="exist" style="text-align: center;">
      <el-image :src="image.loading"></el-image>
    </div>
    <div v-else>
      <el-row>
        <!-- 左半部分 -->
        <el-col :span="14" style="margin-top: 4em; text-align: right;">
          <div>
            <div>
              <el-image :src="image.logo"></el-image>
            </div>
            <div>
              <span class="banner-text">商品美·种类多·欢迎选购</span>
            </div>
            <div></div>
            <el-image :src="image.register"></el-image>
          </div>
        </el-col>
        <!-- 分割线 -->
        <el-col :span="1" style="margin-top: 2em; text-align: center;">
          <el-image :src="image.interval"></el-image>
        </el-col>
        <!-- 右半部分 -->
        <el-col :span="9" style="width: 22em; margin-top: 4em;">
          <div>
            <!-- 标题栏 -->
            <el-row style="line-height: 3em;">
              <el-col :span="18">
                <span class="register-text">绑定账号</span>
              </el-col>
            </el-row>
            <!-- 注册表单 -->
            <el-form size="mini" label-width="6em" :model="form" :rules="rules" ref="registerForm">
              <el-form-item label="手机号:" prop="mobile">
                <el-input v-model="form.mobile"></el-input>
              </el-form-item>
              <el-form-item label="密码:" prop="password">
                <el-input v-model="form.password" type="password" auto-complete="off"></el-input>
              </el-form-item>
              <el-form-item label="验证码:" prop="sms_code">
                <span style="width: 20em;">
                  <el-input style="width: 10em; margin-right:1em;" v-model="form.sms_code"></el-input>
                  <el-button
                    style="width: 8em; text-align: center;"
                    @click="getSmsCode"
                    type="primary"
                    :disabled="send_flag"
                  >{{ send_tips }}</el-button>
                </span>
              </el-form-item>
              <el-form-item style="text-align: center; margin-top: 0px;" label-width="0">
                <el-button type="danger" size="medium" style="width: 20em;" @click="submit">保&nbsp;存</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-col>
      </el-row>
      <!-- 分割线 -->
      <el-divider></el-divider>
      <!-- footer部分 -->
      <Footer></Footer>
    </div>
  </div>
</template>

<script>
import Footer from "@/components/Footer.vue";

export default {
  data() {
    return {
      // 图片路径。引用本地图片时，将图片作为对象导入才能绑定
      image: {
        logo: require("../assets/images/logo.png"),
        register: require("../assets/images/register_banner.png"),
        interval: require("../assets/images/interval_line.png"),
        loading: require("../assets/images/loading.gif")
      },

      // 发送短信按钮标识及文本
      send_flag: false,
      send_tips: "发送验证码",

      // 绑定表单
      form: {
        mobile: "",
        password: "",
        sms_code: "",
        openid: ""
      },

      // 表单校验规则
      rules: {
        password: [
          {
            required: true,
            message: "请输入密码",
            trigger: "blur"
          }
        ],
        mobile: [
          {
            required: true,
            pattern: /^1[3-9]{1}\d{9}$/,
            message: "手机号码不合法",
            trigger: "blur"
          }
        ],
        sms_code: [
          {
            required: true,
            pattern: /^[0-9]{6}$/,
            message: "验证码格式错误",
            trigger: "blur"
          }
        ]
      },

      // QQ用户是否存在
      exist: true
    };
  },
  mounted() {
    this.checkUser();
  },
  methods: {
    // 获取短信验证码
    getSmsCode() {
      let that = this;
      if (that.form.mobile) {
        // 判断是否已经发了短信
        if (that.send_flag) {
          return;
        }

        that.$axios.get("sms_codes/" + that.form.mobile, {}).then(() => {
          // 短信发送成功后，置灰按钮，倒计时60秒，60秒后允许用户再次点击发送短信验证码的按钮
          that.send_flag = true;
          let num = 60;
          // 设置一个计时器
          let timer = setInterval(
            () => {
              if (num == 1) {
                // 如果计时器到最后, 清除计时器对象
                clearInterval(timer);
                // 将点击获取验证码的按钮展示的文本回复成原始文本
                that.send_tips = "发送验证码";
                // 将点击按钮的onclick事件函数恢复回去
                that.send_flag = false;
              } else {
                num -= 1;
                // 展示倒计时信息
                that.send_tips = num + "秒";
              }
            },
            1000,
            60
          );
        });
      } else {
        that.$message.error("请先填写手机号！");
      }
    },
    // 提交绑定表单。提交表单是不论是QQ还是钉钉都走QQ的绑定逻辑，二者在后端处理方式相同
    submit() {
      this.$refs.registerForm.validate(valid => {
        if (valid) {
          let that = this;
          that.$axios.post("oauth/qq/user/", that.form).then(res => {
            // 绑定成功时，状态码为200
            //注册成功后，在本地保存token,id,username等信息
            that.$router.commit("setStatus", {
              username: res.data.username,
              token: res.data.token
            });

            // 跳转页面。根据跳转过来的页面，登陆成功后，跳转回去；否则进入主页
            that.$router.replace(that.$route.query.redirect || "/");
          });
        }
        return false;
      });
    },
    // 获取回调地址中的字段的值
    getCode(name) {
      let url = window.location.href;

      let params = url.substr(url.lastIndexOf("?") + 1).split("&");
      for (let i = 0; i < params.length; i++) {
        let param = params[i];
        let key = param.split("=")[0];
        let value = param.split("=")[1];
        if (key === name) {
          return value;
        }
      }
    },
    // 回调时自动发起请求，检查当前用户是否绑定
    checkUser() {
      let that = this;

      // 获取来源地址，利用回调地址中的state参数来区分是QQ登陆还是钉钉登陆
      let state = that.getCode("state");

      if (state === "STATE") {
        that.$axios
          .get("oauth/dt/user/", { params: { code: that.getCode("code") } })
          .then(res => {
            if (res.data.openid) {
              // 如果openid有值说明之前没有绑定过网站账户，此时设置回调页面进入绑定界面
              that.exist = false;
              that.form.openid = res.data.openid;
            } else {
              // 拿到保存信息，然后返回到登陆前的页面
              sessionStorage.clear(); // sessionStorage关闭浏览器即清除
              localStorage.clear(); // 永久保存
              sessionStorage.token = res.data.token;
              sessionStorage.username = res.data.username;
              sessionStorage.user_id = res.data.id;

              that.$store.commit("setStatus", {
                username: res.data.username,
                token: res.data.token
              });
              // 返回起始页
              that.$router.replace(that.$route.query.redirect || "/");
            }
          });
      } else {
        that.$axios
          .get("oauth/qq/user", { params: { code: that.getCode("code") } })
          .then(res => {
            if (res.data.openid) {
              // 如果openid有值说明该QQ号之前没有绑定过网站账户，此时设置回调页面进入绑定界面
              that.exist = false;
              that.form.openid = res.data.openid;
            } else {
              // 拿到保存信息，然后返回到登陆前的页面
              sessionStorage.clear(); // sessionStorage关闭浏览器即清除
              localStorage.clear(); // 永久保存
              sessionStorage.token = res.data.token;
              sessionStorage.username = res.data.username;
              sessionStorage.user_id = res.data.id;

              that.$store.commit("setStatus", {
                username: res.data.username,
                token: res.data.token
              });
              // 返回起始页
              that.$router.replace(that.$route.query.redirect || "/");
            }
          });
      }
    }
  },
  components: {
    Footer
  }
};
</script>

<style scoped>
.banner-text {
  color: red;
}
.register-text {
  font-size: 1.5em;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  color: grey;
}
.el-input {
  width: 20em;
}
.el-form-item {
  padding-bottom: 2em;
}
.el-form {
  background-color: rgb(180, 202, 206);
  border-radius: 5px;
  padding-top: 2em;
}
</style>