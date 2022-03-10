<!--
 * @Author: flwfdd
 * @Date: 2022-02-21 14:18:44
 * @LastEditTime: 2022-03-10 20:10:44
 * @Description: 
 * _(:з」∠)_
-->
<template>
  <v-container>
    <v-card class="ma-4">
      <v-card-text>
        <v-alert v-if="ok == -1" text color="blue" class="text-center"
          >未登录</v-alert
        >
        <v-alert v-else-if="ok == 1" text color="green" class="text-center"
          >已登录</v-alert
        >
        <v-alert v-else text color="red" class="text-center">登陆失败</v-alert>

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
          :disabled="ok == -1"
          :loading="ok == -1"
          >登陆</v-btn
        >
      </v-card-text>
    </v-card>

    <v-card class="ma-4">
      <v-card-text>
        Tips: 使用统一身份认证的账号和密码登录，密码不会被保存至服务器。BITself 奉行「前端匿名」理念，不会主动显示出任何个人信息。
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { encryptPassword } from "@/components/EncryptPassword";

export default {
  name: "LoginView",
  data: () => ({
    username: "",
    password: "",
    ok: -1,
    show_password:false,
  }),
  methods: {
    Login() {
      this.ok = -1;
      this.$store.commit("set_webvpn_login", this.username, this.password);
      let url = this.$store.state.api_url + "/login/init/";
      this.$axios
        .get(url)
        .then((res) => {
          let salt = res.data.salt;
          let execution = res.data.execution;
          let password = encryptPassword(this.password, salt);
          let cookie = res.data.cookie;
          this.$store.commit("set_webvpn_cookie", cookie);

          let url = this.$store.state.api_url + "/login/";
          this.$axios
            .post(url, {
              username: this.username,
              password: password,
              execution: execution,
              cookie: cookie,
            })
            .then((res) => {
              this.ok = 1;
              this.$store.commit("set_fake_cookie", res.headers["fake_cookie"]);
            })
            .catch((err) => {
              console.log(err);
              this.ok = 0;
            });
        })
        .catch((err) => {
          console.log(err);
          this.ok = 0;
        });
    },
    CheckLogin() {
      this.$axios
        .get(this.$store.state.api_url)
        .then(() => {
          this.ok = 1;
        })
        .catch(() => {
          this.ok = 0;
        });
    },
  },
  created() {
    this.CheckLogin();
  },
};
</script>
