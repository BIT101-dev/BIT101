<!--
 * @Author: flwfdd
 * @Date: 2022-02-20 22:45:07
 * @LastEditTime: 2022-02-21 12:44:20
 * @Description: 
 * _(:з」∠)_
-->
<template>
  <v-container>
    <v-row justify="center" class="my-12 ">
      <h1 class="cyan--text">欢迎来到BITself</h1>
    </v-row>

    <v-row justify="center" class="mx-2">
      <HitokotoText class="blue-grey--text"/>
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
