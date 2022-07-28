<!--
 * @Author: flwfdd
 * @Date: 2022-05-28 01:26:29
 * @LastEditTime: 2022-07-28 16:19:37
 * @Description: 主页
 * _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import { onMounted, ref } from 'vue';

const carousel = ref([])
function LoadCarousel() {
  http.get("/variable/?obj=carousel").then((res) => {
    carousel.value = res.data;
  })
}

onMounted(() => {
  LoadCarousel();
})
</script>

<template>
  <div class="container" style="text-align: center;">
    <n-carousel autoplay show-arrow>
      <a v-for="i in carousel" :href="i['url']" :target="i['url'] ? '' : '_blank'"><img :src="i['img']"
          style="width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;"></a>
    </n-carousel>
  </div>

</template>


