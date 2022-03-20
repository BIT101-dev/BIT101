<!--
 * @Author: flwfdd
 * @Date: 2022-03-16 22:28:42
 * @LastEditTime: 2022-03-18 15:52:51
 * @Description: 
 * _(:з」∠)_
-->
<template>
  <v-img :src="low_src" :lazy-src="lazy_src">
    <template v-slot:placeholder>
      <v-row class="fill-height ma-0" align="center" justify="center">
        <v-progress-circular
          indeterminate
          color="blue-grey lighten-4"
        ></v-progress-circular>
      </v-row>
    </template>
  </v-img>
</template>

<script>
export default {
  name: "SelfImg",
  props: ["src"],
  data: () => ({
    ori_src: "",
    lazy_src: "",
    low_src: "",
  }),
  methods: {
    UpdateSrc() {
      if (this.src) {
        this.ori_src = this.$store.state.img_url + this.src;
        this.low_src = this.ori_src + "!low";
        this.lazy_src = this.ori_src + "!lazy";
      }
    },
  },
  watch: {
    src() {
      this.UpdateSrc();
    },
  },
  created() {
    this.UpdateSrc();
  },
};
</script>