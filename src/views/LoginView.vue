<!--
 * @Author: flwfdd
 * @Date: 2022-02-21 14:18:44
 * @LastEditTime: 2022-03-13 10:10:07
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
        Tips: 使用统一身份认证的账号和密码登录，密码不会被发送到服务器。
        BITself 奉行「前端匿名」理念，不会主动显示出任何个人信息。
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { Login } from "@/components/GlobalMethod";

export default {
  name: "LoginView",
  data: () => ({
    username: "",
    password: "",
    ok: -1,
    show_password: false,
  }),
  methods: {
    Login() {
      this.ok = -1;
      Login(this.username, this.password).then((ok) => {
        this.ok = ok;
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
