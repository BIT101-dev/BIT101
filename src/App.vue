<!--
 * @Author: flwfdd
 * @Date: 2022-02-20 22:45:07
 * @LastEditTime: 2022-02-21 17:47:35
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
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>

    <v-footer app>
      <!-- -->
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: "App",

  data: () => ({
    drawer: false,
    items: [
      { title: "主页", icon: "home", link: "/" },
      { title: "登录", icon: "fingerprint", link: "/login" },
      { title: "成绩", icon: "school", link: "/score" },
      { title: "关于", icon: "info", link: "/about" },
    ],
  }),
  methods: {
    Go(url) {
      this.$router.push(url);
    },
  },
};
</script>
