<!--
 * @Author: flwfdd
 * @Date: 2022-02-20 22:45:07
 * @LastEditTime: 2022-03-20 11:33:38
 * @Description: 
 * _(:з」∠)_
-->
<template>
  <v-container>
    <v-row justify="center" class="mt-12">
      <h1 class="cyan--text">欢迎来到BITself</h1>
    </v-row>

    <v-row justify="center" class="mb-12">
      <v-chip
        color="pink lighten-3"
        small
        outlined
        href="https://space.bilibili.com/27482524"
        target="_blank"
      >
        <v-icon small>mdi-television-classic</v-icon>bilibili
      </v-chip>
      <v-chip
        color="cyan lighten-3"
        small
        outlined
        href="https://github.com/flwfdd/BITself"
        target="_blank"
      >
        <v-icon small>mdi-github</v-icon>Github
      </v-chip></v-row
    >

    <v-row justify="center" class="mx-2">
      <HitokotoText class="blue-grey--text" />
    </v-row>
  </v-container>
</template>

<script>
// @ is an alias to /src
import HitokotoText from "@/components/HitokotoText.vue";

export default {
  name: "HomeView",
  components: {
    HitokotoText,
  },
};
</script>
