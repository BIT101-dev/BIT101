<!--
 * @Author: flwfdd
 * @Date: 2022-02-20 22:45:07
 * @LastEditTime: 2022-03-19 23:20:38
 * @Description: 
 * _(:з」∠)_
-->
<template>
  <v-app>
    <v-navigation-drawer app v-model="drawer">
      <v-list-item>
        <v-list-item-avatar>
          <img alt="Vue logo" src="./assets/logo.png" />
        </v-list-item-avatar>
        <v-list-item-title>BITself</v-list-item-title>
        <v-spacer></v-spacer>
      </v-list-item>

      <v-divider></v-divider>

      <v-list dense nav>
        <v-list-item-group color="cyan">
          <v-list-item
            v-for="item in items"
            :key="item.title"
            @click="Go(item.link)"
          >
            <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="cyan">
      <v-app-bar-nav-icon
        color="white"
        @click="drawer = !drawer"
      ></v-app-bar-nav-icon>
      <v-app-bar-title class="white--text">BITself</v-app-bar-title>
      <v-spacer/>
      <v-app-bar-nav-icon color="white" @click="$router.go(-1)">
              <v-icon>arrow_back</v-icon>
      </v-app-bar-nav-icon>
      <v-app-bar-nav-icon color="white" @click="$router.go(0)">
              <v-icon>refresh</v-icon>
      </v-app-bar-nav-icon>
    </v-app-bar>

    <v-main>
      <keep-alive>
        <router-view :key="$route.fullPath"></router-view>
      </keep-alive>
    </v-main>

    <v-footer app>
      <!-- -->
    </v-footer>

    <v-snackbar v-model="snackbar">
      {{ snackbar_msg }}
      <template v-slot:action="{ attrs }">
        <v-btn color="pink" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
export default {
  name: "App",

  data: () => ({
    drawer: false,
    items: [
      { title: "主页", icon: "home", link: "/" },
      { title: "我的", icon: "fingerprint", link: "/my" },
      { title: "成绩", icon: "school", link: "/score" },
      { title: "评教", icon: "class", link: "/course" },
      { title: "关于", icon: "info", link: "/about" },
    ],
    snackbar: false,
  }),
  methods: {
    Go(url) {
      this.$router.push(url);
    },
  },
  computed:{
    snackbar_msg(){
      return this.$store.state.msg;
    }
  },
  watch:{
    snackbar_msg(){
      this.snackbar=true;
    }
  }
};
</script>
