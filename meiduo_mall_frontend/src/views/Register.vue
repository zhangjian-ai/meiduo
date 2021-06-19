<template>
  <div>
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
              <span class="register-text">用户注册</span>
            </el-col>
            <el-col :span="6" style="text-align: right;">
              <!-- click事件直接绑定router内置函数完成页面跳转 -->
              <el-button type="text" @click="$router.push({ name: 'login' })">
                登陆
                <i class="el-icon-d-arrow-right el-icon--right"></i>
              </el-button>
            </el-col>
          </el-row>
          <el-divider></el-divider>

          <!-- 注册表单 -->
          <el-form size="mini" label-width="6em" :model="form" :rules="rules" ref="registerForm">
            <el-form-item label="用户名:" prop="username">
              <el-input v-model="form.username"></el-input>
            </el-form-item>
            <el-form-item label="密码:" prop="password">
              <el-input v-model="form.password" type="password" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="确认密码:" prop="password2">
              <el-input
                v-model="form.password2"
                type="password"
                auto-complete="off"
                ref="password2"
              ></el-input>
            </el-form-item>
            <el-form-item label="手机号:" prop="mobile">
              <el-input v-model="form.mobile"></el-input>
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
            <el-form-item style="text-align: left;" label-width="6em" prop="allow">
              <el-checkbox v-model="form.allow" true-label="true">同意 “张老师的使用协议”</el-checkbox>
            </el-form-item>
            <el-form-item style="text-align: center; margin-top: 0px;" label-width="0">
              <el-button type="danger" size="medium" style="width: 20em;" @click="submit">立即注册</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-col>
    </el-row>
    <!-- footer部分 -->
    <Footer></Footer>
  </div>
</template>

<script>
import Footer from "@/components/Footer.vue";

export default {
  name: "Register",
  data() {
    // 校验两次密码输入是否相同，校验成功时一定要回调callback()。否则会导致全局校验通过后不继续执行
    const check_pwd = (rule, value, callback) => {
      if (this.form.password === value) {
        callback();
      } else {
        this.form.password2 = "";
        // 当校验不过时，确认密码框自动获得焦点
        // this.$refs.password2.focus();
        callback(new Error("两次输入的密码不一致，请重新输入"));
      }
    };
    const check_username = (rule, value, callback) => {
      this.$axios
        .get("users/" + value + "/count/")
        .then(res => {
          if (res.data.count > 0) {
            callback(new Error("用户名已存在"));
          }
          callback();
        })
        .catch(err => {
          this.$message.error(err.message);
        });
    };
    const check_mobile = (rule, value, callback) => {
      this.$axios
        .get("users/" + value + "/count/")
        .then(res => {
          if (res.data.count > 0) {
            callback(new Error("该手机号已经注册"));
          }
          callback();
        })
        .catch(err => {
          this.$message.error(err.message);
        });
    };

    return {
      // 图片路径。引用本地图片时，将图片作为对象导入才能绑定
      image: {
        logo: require("../assets/images/logo.png"),
        register: require("../assets/images/register_banner.png"),
        interval: require("../assets/images/interval_line.png")
      },

      // 发送短信按钮标识及文本
      send_flag: false,
      send_tips: "发送验证码",

      // 注册表单
      form: {
        username: "",
        password: "",
        password2: "",
        mobile: "",
        sms_code: "",
        allow: ""
      },

      // 表单校验规则
      rules: {
        username: [
          {
            required: true,
            pattern: /^\w{5,20}$/,
            message: "用户名应由字母数字或下划线组成的5～20位字符",
            trigger: "blur"
          },
          { validator: check_username, trigger: "blur" }
        ],
        password: [
          {
            required: true,
            pattern: /^\w{8,20}$/,
            message: "密码应由字母数字或下划线组成的8～20位字符",
            trigger: "blur"
          }
        ],
        password2: [
          {
            required: true,
            message: "确认密码为必填项",
            trigger: "blur"
          },
          { validator: check_pwd, trigger: "blur" }
        ],
        mobile: [
          {
            required: true,
            pattern: /^1[3-9]{1}\d{9}$/,
            message: "手机号码不合法",
            trigger: "blur"
          },
          { validator: check_mobile, trigger: "blur" }
        ],
        sms_code: [
          {
            required: true,
            pattern: /^[0-9]{6}$/,
            message: "验证码错误",
            trigger: "blur"
          }
        ],
        allow: [
          { required: true, message: "请勾选使用协议", trigger: "change" }
        ]
      }
    };
  },
  mounted() {},
  methods: {
    // 获取短信验证码
    getSmsCode() {
      let that = this;
      if (that.form.mobile) {
        // 判断是否已经发了短信
        if (that.send_flag) {
          return;
        }

        that.$axios
          .get("sms_codes/" + that.form.mobile + "/")
          .then(res => {
            if (res.status == 200) {
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
            }
          })
      } else {
        that.$message.error("请先填写手机号！");
      }
    },
    // 提交注册表单
    submit() {
      this.$refs.registerForm.validate(valid => {
        if (valid) {
          let that = this;
          that.$axios
            .post("users/", that.form)
            .then(res => {
              // 注册成功时，状态码为201
              // 注册成功后，保存token信息
              sessionStorage.clear(); // sessionStorage关闭浏览器即清除
              localStorage.clear(); // 永久保存

              sessionStorage.token = res.data.token;
              sessionStorage.username = res.data.username;
              sessionStorage.user_id = res.data.id;

              this.$store.commit("setStatus", {
                username: res.data.username,
                token: res.data.token
              });

              // 跳转页面。根据跳转过来的页面，登陆成功后，跳转回去；否则进入主页
              that.$router.replace(that.$route.query.redirect || "/");
            })
            .catch(err => {
              that.$message.error("服务器错误");
              that.$message.error(err.message);
            });
        } else {
          return false;
        }
      });
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
  margin-top: 2em;
}
.el-form {
  padding-bottom: 1em;
}
.el-divider {
  margin: 0;
  padding: 0;
}
</style>