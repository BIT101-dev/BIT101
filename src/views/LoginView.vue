<!--
 * @Author: flwfdd
 * @Date: 2022-02-21 14:18:44
 * @LastEditTime: 2022-02-22 14:54:13
 * @Description: 
 * _(:з」∠)_
-->
<template>
  <v-container>
    <v-card class="ma-5">
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
          v-model="user"
          label="你的名字。"
        ></v-text-field>
        <v-text-field
          color="cyan"
          outlined
          v-model="password"
          label="你的密码。"
        ></v-text-field>

        <v-btn block outlined color="cyan" @click="Login" :disabled="ok == -1"
          >登陆</v-btn
        >
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { encryptPassword } from "@/components/EncryptPassword";

export default {
  name: "LoginView",
  data: () => ({
    user: "",
    password: "",
    ok: -1,
  }),
  methods: {
    Login() {
      this.ok = -1;
      // 重新登陆
      this.$store.commit("set_cookie", "");
      let url =
        this.$store.state.base_url +
        "/https/77726476706e69737468656265737421fcf84695297e6a596a468ca88d1b203b/authserver/login?service=https%3A%2F%2Fwebvpn.bit.edu.cn%2Flogin%3Fcas_login%3Dtrue";
      this.$axios
        .get(url)
        .then((res) => {
          this.$store.commit("set_cookie", res.headers["fake_cookie"]);

          let parser = new DOMParser();
          let dom = parser.parseFromString(res.data, "text/html");
          let salt = dom.querySelector("#pwdFromId > #pwdEncryptSalt").value;
          let execution = dom.querySelector("#pwdFromId > #execution").value;
          let password = encryptPassword(this.password, salt);

          let form_data = {
            username: this.user,
            password: password,
            captcha: "",
            _eventId: "submit",
            cllt: "userNameLogin",
            dllt: "generalLogin",
            lt: "",
            execution: execution,
          };
          let FormDataBody = new FormData();
          for (let i in form_data) {
            FormDataBody.set(i, form_data[i]);
          }

          this.$axios
            .post(url, FormDataBody, {
              headers: {
                "Content-Type": "application/x-www-form-urlencoded",
              },
            })
            .then(() => {
              this.CheckLogin();
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
        .get(this.$store.state.base_url + "/login?cas_login=true")
        .then((res) => {
          if (res.data.search("帐号登录或动态码登录") == -1) {
            this.ok = 1;
          } else {
            this.ok = 0;
          }
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
