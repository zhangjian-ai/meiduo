<template>
  <div>
    <el-row>
      <el-button type="primary" icon="el-icon-plus" size="mini" @click="show_addrForm">新增收货地址</el-button>
      <span class="tip">
        当前已有
        <span style="color: red; margin: 0.5em;">{{ count }}</span>个收货地址，
        最多添加
        <span style="color: red; margin: 0.5em;">{{ total }}</span>个收货地址
      </span>
    </el-row>
    <el-divider></el-divider>
    <!-- 收货地址列表 -->
    <div style="height: 29em; overflow:auto; width: 50em;">
      <el-row v-for="(address, index) in addresses" :key="address.title">
        <div class="detail">
          <el-row style="margin-left: 4em;">
            <el-col :span="22">
              <span v-if="is_set_title[index]">
                <el-input v-model="input_title" placeholder="输入标题" size="mini"></el-input>&nbsp;
                <el-button type="primary" @click="edit_title(index)" size="mini">确认</el-button>
                <el-button type="info" @click="hide_edit_title" size="mini">取消</el-button>
              </span>
              <span v-else>
                <span style="font-size: 2em;">{{ address.title }}</span>
                <el-button
                  type="text"
                  size="mini"
                  style="margin: 0 2em;"
                  @click="show_edit_title(index)"
                >修改标题</el-button>
                <span v-if="address.is_default">
                  <el-tag type="danger" effect="dark" size="mini">默认地址</el-tag>
                </span>
              </span>
            </el-col>
            <el-col :span="2" style="text-align: right;">
              <el-link :underline="false" @click="delete_address(index)">
                <i class="el-icon-close"></i>
              </el-link>
            </el-col>
          </el-row>
          <el-row>
            <el-row>
              <el-col :span="3" style="text-align: right;">收货人：</el-col>
              <el-col :span="14" style="text-align: left;">{{ address.receiver }}</el-col>
            </el-row>
            <el-row>
              <el-col :span="3" style="text-align: right;">地区：</el-col>
              <el-col
                :span="14"
                style="text-align: left;"
              >{{ address.province }}&nbsp;{{ address.city }}&nbsp;{{ address.district }}</el-col>
            </el-row>
            <el-row>
              <el-col :span="3" style="text-align: right;">详细地址：</el-col>
              <el-col :span="14" style="text-align: left;">{{ address.place }}</el-col>
            </el-row>
            <el-row>
              <el-col :span="3" style="text-align: right;">手机号：</el-col>
              <el-col :span="14" style="text-align: left;">{{ address.mobile }}</el-col>
            </el-row>
            <el-row>
              <el-col :span="3" style="text-align: right;">固定电话：</el-col>
              <el-col :span="14" style="text-align: left;">{{ address.tel }}</el-col>
            </el-row>
            <el-row>
              <el-col :span="3" style="text-align: right;">电子邮箱：</el-col>
              <el-col :span="14" style="text-align: left;">{{ address.email }}</el-col>
            </el-row>
            <el-row>
              <el-col :span="20" style="text-align: right;">
                <el-button @click="edit_address(index)" type="text" size="mini">
                  <i class="el-icon-edit"></i>编辑修改
                </el-button>
              </el-col>
              <el-col :span="3" style="text-align: right;">
                <el-button @click="set_default_address(index)" type="text" size="mini">设为默认地址</el-button>
              </el-col>
            </el-row>
          </el-row>
        </div>
      </el-row>
    </div>

    <!-- 新增和修改地址表单 -->
    <el-dialog :title="title" :visible.sync="dialogVisible" width="36em">
      <el-form :model="addrForm" :rules="rules" label-width="8em" ref="addrForm">
        <el-form-item label="收件人：" prop="receiver">
          <el-input v-model="addrForm.receiver" size="mini"></el-input>
        </el-form-item>
        <el-form-item label="省市区：" required>
          <el-col :span="7">
            <el-form-item prop="province_id">
              <el-select v-model="addrForm.province_id" size="mini">
                <el-option
                  v-for="item in province"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="7">
            <el-form-item prop="city_id">
              <el-select v-model="addrForm.city_id" size="mini">
                <el-option v-for="item in city" :key="item.id" :label="item.name" :value="item.id"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="7">
            <el-form-item prop="district_id">
              <el-select v-model="addrForm.district_id" size="mini">
                <el-option
                  v-for="item in district"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-form-item>
        <el-form-item label="详细地址：" prop="place">
          <el-input v-model="addrForm.place" size="mini"></el-input>
        </el-form-item>
        <el-form-item label="手机：" prop="mobile">
          <el-input v-model="addrForm.mobile" size="mini"></el-input>
        </el-form-item>
        <el-form-item label="固定电话：" prop="tel">
          <el-input v-model="addrForm.tel" size="mini"></el-input>
        </el-form-item>
        <el-form-item label="电子邮箱：" prop="email">
          <el-input v-model="addrForm.email" size="mini"></el-input>
        </el-form-item>
      </el-form>
      <span style="margin-left:28em;">
        <el-button @click="reset_addrForm" size="mini">重 置</el-button>
        <el-button type="primary" @click="submit" size="mini">提 交</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
export default {
  name: "Address",
  data() {
    return {
      // 收货地址数量
      total: 0,
      count: 0,

      // 保存后端返回的地址列表
      addresses: [],

      // 修改标题
      is_set_title: [],
      input_title: "",

      //展示表单
      dialogVisible: false,
      title: "",

      // 省市区数据
      province: [],
      city: [],
      district: [],

      //表单
      addrForm: {
        receiver: "",
        province_id: "",
        city_id: "",
        district_id: "",
        place: "",
        mobile: "",
        tel: "",
        email: ""
      },

      // 表单提交类型  0:新增  1:修改
      type: 0,

      //表单校验规则
      rules: {
        receiver: [
          { required: true, message: "收件人必填项", trigger: "blur" }
        ],
        place: [{ required: true, message: "收件人必填项", trigger: "blur" }],
        mobile: [
          {
            required: true,
            pattern: /^1[3-9]{1}\d{9}$/,
            message: "手机号码不合法",
            trigger: "blur"
          }
        ],
        province_id: [{ required: true, message: "请选择", trigger: "change" }],
        city_id: [{ required: true, message: "请选择", trigger: "change" }],
        district_id: [{ required: true, message: "请选择", trigger: "change" }]
      }
    };
  },
  mounted() {
    this.get_addrsss();
    this.get_province();
  },

  methods: {
    // 获取地址信息
    get_addrsss() {
      this.$api.address().then(res => {
        this.total = res.data.limit;
        this.addresses = res.data.address;
        this.count = this.addresses.length;
      });
    },
    // 展示编辑标题
    show_edit_title(index) {
      this.input_title = this.addresses[index].title;
      for (var i = 0; i < index; i++) {
        this.is_set_title.push(false);
      }
      this.is_set_title.push(true);
    },
    // 隐藏编辑标题
    hide_edit_title() {
      this.is_set_title = [];
    },
    // 修改地址标题
    edit_title(index) {
      let that = this;
      that.$axios
        .put("edit_address_title/", {
          id: that.addresses[index].id,
          title: that.input_title
        })
        .then(res => {
          that.hide_edit_title();
          that.get_addrsss();
          that.$notify({
            type: "success",
            message: res.data.msg
          });
        });
    },
    // 删除地址
    delete_address(index) {
      let that = this;
      that.$axios
        .delete("address/", {
          data: {
            id: that.addresses[index].id
          }
        })
        .then(res => {
          that.get_addrsss();
          that.$notify({
            type: "success",
            message: res.data.msg
          });
        });
    },
    // 获取省级信息
    get_province() {
      ";";
      let that = this;
      that.$axios.get("areas/").then(res => {
        that.province = res.data;
      });
    },
    // 清空表单数据
    reset_addrForm() {
      // 重置表单校验,mouted加载table数据以后，隐藏的弹出框并没有编译渲染紧DOM里
      // 只能重置带有prop且为字段名的表单项
      if (this.$refs.addrForm !== undefined) {
        this.$refs.addrForm.resetFields();
      }
    },
    // 新增地址
    show_addrForm() {
      this.reset_addrForm();
      this.dialogVisible = true;
      this.type = 0;
      this.title = "新增地址";
    },
    // 提交表单
    submit() {
      let that = this;
      that.$refs.addrForm.validate(valid => {
        if (valid) {
          if (that.type === 0) {
            that.$axios.post("address/", that.addrForm).then(res => {
              that.$notify({
                type: "success",
                message: res.data.msg
              });
              that.get_addrsss();
              that.dialogVisible = false;
            });
          }
          if (that.type === 1) {
            that.$axios.put("address/", that.addrForm).then(res => {
              that.$notify({
                type: "success",
                message: res.data.msg
              });
              that.get_addrsss();
              that.dialogVisible = false;
            });
          }
        } else {
          return false;
        }
      });
    },
    // 修改收货地址
    edit_address(index) {
      let that = this;
      // 回填表单
      that.addrForm.receiver = that.addresses[index].receiver;
      that.addrForm.province_id = that.addresses[index].province_id;
      that.addrForm.city_id = that.addresses[index].city_id;
      that.addrForm.district_id = that.addresses[index].district_id;
      that.addrForm.place = that.addresses[index].place;
      that.addrForm.mobile = that.addresses[index].mobile;
      that.addrForm.tel = that.addresses[index].tel;
      that.addrForm.email = that.addresses[index].email;
      // 修改地址时，加入地址id
      that.addrForm.id = that.addresses[index].id;
      that.addrForm.title = that.addresses[index].title;

      that.dialogVisible = true;
      that.title = "修改收货地址";
      that.type = 1;
    },
    // 设为默认地址
    set_default_address(index) {
      let that = this;
      if (that.addresses[index].is_default === true) {
        this.$notify({
          type: "warning",
          message: "当前地址已经是默认地址"
        });
        return;
      }
      that.$axios
        .put("address/", {
          id: that.addresses[index].id,
          is_default: true
        })
        .then(res => {
          that.$notify({
            type: "success",
            message: res.data.msg
          });
          that.get_addrsss();
        });
    }
  },
  // 监听：选择了省就查市，选择了市就查区
  watch: {
    "addrForm.province_id": function() {
      let that = this;
      if (that.addrForm.province_id) {
        that.$axios
          .get("areas/" + that.addrForm.province_id + "/")
          .then(res => {
            that.city = res.data.subs;
            that.district = [];
          })
          .catch(() => {
            that.city = [];
            that.district = [];
          });
      }
    },
    "addrForm.city_id": function() {
      let that = this;
      if (that.addrForm.city_id) {
        that.$axios
          .get("areas/" + that.addrForm.city_id + "/")
          .then(res => {
            that.district = res.data.subs;
          })
          .catch(() => {
            that.district = [];
          });
      }
    }
  }
};
</script>
<style scoped>
.el-divider {
  margin: 0.5em;
  margin-left: 0;
  padding: 0;
}
.tip {
  font-size: 0.5em;
  margin: 2em;
}
.el-row {
  margin: 0.25em;
}
.detail {
  font-size: 0.5em;
  border: 0.5px solid rgb(176, 176, 240);
  margin: 0.5em;
  padding: 0.5em;
  border-radius: 0.5em;
}
.el-input {
  width: 32em;
  margin-right: 1em;
}
.button {
  text-align: right;
  padding-right: 3em;
}
.el-select {
  width: 8em;
}
</style>