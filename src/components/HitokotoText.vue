<!--
 * @Author: flwfdd
 * @Date: 2022-02-20 22:45:07
 * @LastEditTime: 2022-02-20 23:33:20
 * @Description: 
 * _(:з」∠)_
-->
<template>
  <h4>{{ hitokoto }}</h4>
</template>

<script>
export default {
  name: "HitokotoText",

  data: () => ({
    hitokoto: "2333",
  }),
  methods: {
    UpHitokoto() {
      this.$axios.get("https://v1.hitokoto.cn/").then((res) => {
        this.hitokoto = res.data.hitokoto + "  ——" + res.data.from;
      });
    },
  },
  created() {
    this.UpHitokoto();
    setInterval(this.UpHitokoto, 10 * 1000);
  },
};
</script>
