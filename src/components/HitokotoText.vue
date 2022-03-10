<!--
 * @Author: flwfdd
 * @Date: 2022-02-20 22:45:07
 * @LastEditTime: 2022-03-10 19:54:39
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
    hitokoto: "I offer you the BITterness of a man who has looked long and long at the lonely moon.",
  }),
  methods: {
    UpHitokoto() {
      this.$axios.get("https://v1.hitokoto.cn/").then((res) => {
        this.hitokoto = res.data.hitokoto + "  ——" + res.data.from;
      });
    },
  },
  created() {
    setInterval(this.UpHitokoto, 10 * 1000);
  },
};
</script>
