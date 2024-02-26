<!--
 * @Author: flwfdd
 * @Date: 2022-05-28 01:26:29
 * @LastEditTime: 2024-02-26 17:11:18
 * @Description: 主页
 * _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import { onMounted, ref } from 'vue';
import Billboard from '@/components/Billboard.vue';
import { OpenLink } from '@/utils/tools';

const carousel_data = ref([])
function LoadCarousel() {
  http.get("/variables?obj=carousel").then((res) => {
    carousel_data.value = JSON.parse(res.data.data);
  })
}

const billboard_data = ref([])
function LoadBillboard() {
  http.get("/variables?obj=billboard").then((res) => {
    billboard_data.value = JSON.parse(res.data.data);
  })
}

onMounted(() => {
  LoadCarousel();
  LoadBillboard();
})
</script>

<style scoped>
a {
  text-decoration: none;
}

h2 {
  margin: 4px 0 4px 0;
  text-decoration: underline #FF8533;
}
</style>

<template>
  <div class="container">
    <n-space vertical>
      <n-carousel autoplay show-arrow style="border-radius:11px;">
        <img v-for="i in carousel_data" @click="OpenLink(i['url'])" :src="i['img']"
          style="width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;"
          :style="{ 'cursor': i['url'] ? 'pointer' : 'auto' }">
      </n-carousel>

      <n-alert closable :show-icon="false">
        <div style="font-size:14px;">Tips:点击左上角的≡可以打开菜单哟！</div>
      </n-alert>

      <Billboard :data="billboard_data"></Billboard>
    </n-space>
    <br/>
  </div>

</template>


