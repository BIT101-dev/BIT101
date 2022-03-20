<!--
 * @Author: flwfdd
 * @Date: 2022-02-21 14:18:44
 * @LastEditTime: 2022-03-18 15:58:30
 * @Description: 
 * _(:з」∠)_
-->
<template>
  <v-container>
    <v-card class="ma-4">
      <v-alert v-if="status == 0" text color="red" class="text-center"
        >登陆失败</v-alert
      >
      <v-alert v-else-if="status == 1" text color="green" class="text-center"
        >已登录</v-alert
      >
      <v-alert v-else text color="blue" class="text-center">未登录</v-alert>

      <v-card-text v-if="status != 1">
        <v-text-field
          color="cyan"
          outlined
          v-model="username"
          label="你的账号。"
        ></v-text-field>
        <v-text-field
          color="cyan"
          outlined
          v-model="password"
          label="你的密码。"
          :append-icon="show_password ? 'mdi-eye' : 'mdi-eye-off'"
          :type="show_password ? 'text' : 'password'"
          @click:append="show_password = !show_password"
        ></v-text-field>

        <v-btn
          block
          outlined
          color="cyan"
          @click="Login"
          :disabled="status == -1"
          :loading="status == -1"
          >登陆</v-btn
        >
      </v-card-text>

      <v-container v-else class="pa-4">
        <v-row>
          <v-col>
            <h1 class="cyan--text">你好呀ヾ(´▽｀))</h1>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-avatar @click="upload_dialog=1">
              <SelfImg :src="info.avatar"></SelfImg>
            </v-avatar>
            uid: #{{ info.id }}
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-text-field
              v-model="info.nickname"
              label="你的名字。"
              color="cyan"
              :readonly="nickname_readonly"
              :append-outer-icon="nickname_readonly ? 'edit' : 'check'"
              @click:append-outer="EditName()"
              hint="其实是昵称"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-textarea
              v-model="info.motto"
              color="cyan"
              outlined
              label="格言"
              :readonly="motto_readonly"
              :append-outer-icon="motto_readonly ? 'edit' : 'check'"
              @click:append-outer="EditMotto()"
              hint="介绍一下自己吧"
            ></v-textarea>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-btn block outlined color="red" @click="logout_dialog=true">登出</v-btn>
          </v-col>
        </v-row>
      </v-container>
      <v-alert text color="red" class="text-center ma-0" dense
        >上网不涉密 涉密不上网</v-alert
      >
    </v-card>

    <v-card class="ma-4">
      <v-card-text>
        Tips: 使用统一身份认证的账号和密码登录，密码不会被发送至服务器。 BITself
        奉行「前端匿名」理念，不会主动显示任何个人信息。
      </v-card-text>
    </v-card>

    <v-dialog v-model="upload_dialog">
      <UploadImage @uploaded="UploadedHandler" />
    </v-dialog>

    <v-dialog
      v-model="logout_dialog"
      max-width="424"
    >
      <v-card>
        <v-card-title>
          汝真去离耶？
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="cyan"
            text
            @click="logout_dialog = false"
          >
            取消
          </v-btn>
          <v-btn
            color="red"
            text
            @click="Logout(),logout_dialog=false"
          >
            确定
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { Login } from "@/components/GlobalMethod";
import UploadImage from "@/components/UploadImage.vue";
import SelfImg from "@/components/SelfImg.vue";

export default {
  name: "MyView",
  components: {
    UploadImage,
    SelfImg,
  },
  data: () => ({
    username: "",
    password: "",
    status: -2,
    show_password: false,
    info: { nickname: "", avatar: "", id: 0, motto: "" },
    nickname_readonly: true,
    upload_dialog: false,
    motto_readonly: true,
    logout_dialog:false,
  }),
  methods: {
    Login() {
      this.status = -1;
      Login(this.username, this.password).then((ok) => {
        this.status = ok;
        if (ok == 1) this.GetInfo();
      });
    },
    GetInfo() {
      this.$axios
        .get(this.$store.state.api_url + "/my/info/")
        .then((res) => {
          this.info = res.data;
          this.status = 1;
        })
        .catch(() => {
          this.status = -2;
        });
    },
    Logout() {
      this.$store.commit("set_fake_cookie", "");
      this.$store.commit("set_webvpn_cookie", "");
      this.$store.commit("set_webvpn_login", {
        username: "",
        password: "",
      });
      this.status = -2;
    },
    EditInfo() {
      this.$axios
        .get(this.$store.state.api_url + "/my/edit_info/", {
          params: {
            nickname: this.info.nickname,
            avatar: this.info.avatar,
            motto: this.info.motto,
          },
        })
        .then(() => {
          this.$store.commit("msg", "更改成功OvO");
        })
        .catch(() => {
          this.$store.commit("msg", "更改失败Orz");
        });
    },
    EditName() {
      if (!this.nickname_readonly) {
        let nickname = this.info.nickname;
        if (nickname.length == 0) {
          this.$store.commit("msg", "不要无名氏捏(＠_＠;)");
        } else if (nickname.length > 24) {
          this.$store.commit("msg", "太长啦(＠_＠;)");
        } else {
          this.EditInfo();
        }
      }
      this.nickname_readonly = !this.nickname_readonly;
    },
    EditMotto() {
      if (!this.motto_readonly) {
        let motto = this.info.motto;
        if (motto.length == 0) {
          this.$store.commit("msg", "不要空空如也(＠_＠;)");
        } else {
          this.EditInfo();
        }
      }
      this.motto_readonly = !this.motto_readonly;
    },
    UploadedHandler(list) {
      this.info.avatar = list[0];
      this.upload_dialog = false;
      this.EditInfo();
    },
  },
  created() {
    this.GetInfo();
  },
};
</script>
