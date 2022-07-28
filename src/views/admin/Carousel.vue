<!--
 * @Author: flwfdd
 * @Date: 2022-07-28 13:12:52
 * @LastEditTime: 2022-07-28 16:05:04
 * @Description: 
 * _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import { onMounted, reactive, ref } from 'vue';


const carousel_item_template = {
  "img": "",
  "url": "",
}

const carousel = reactive({
  input: "",
  preview: [],
})

function Add() {
  let x = JSON.parse(carousel.input);
  x.push(carousel_item_template);
  carousel.input = JSON.stringify(x, null, 2);
}

function Preview() {
  carousel.preview = JSON.parse(carousel.input);
}

function Load() {
  http.get("/variable/?obj=carousel").then((res) => {
    carousel.preview = res.data;
    carousel.input = JSON.stringify(res.data, null, 2);
  })
}

function Submit() {
  http.post("/variable/", {
    obj: 'carousel',
    data: JSON.stringify(carousel.preview),
  })
}

onMounted(() => { Load() })

</script>

<template>
  <div class="container">
    <n-space vertical>
      <h2>轮播图设置</h2>
      <n-carousel autoplay show-arrow>
        <a v-for="i in carousel.preview" :href="i['url']" :target="(i['url']&&i['url'][0]=='/')?'':'_blank'"><img :src="i['img']"
          style="width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;"></a>
      </n-carousel>
      <n-input v-model:value="carousel.input" type="textarea" placeholder="JSON" rows="11" />
      <n-button @click="Add" block>添加</n-button>
      <n-button @click="Preview" block>预览</n-button>
      <n-button @click="Submit" block>提交</n-button>
    </n-space>
  </div>

</template>