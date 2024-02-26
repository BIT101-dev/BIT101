<!--
 * @Author: flwfdd
 * @Date: 2022-07-28 13:12:52
 * @LastEditTime: 2024-02-26 17:09:21
 * @Description: 
 * _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import { OpenLink } from '@/utils/tools';
import { onMounted, reactive } from 'vue';


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
  http.get("/variables?obj=carousel").then((res) => {
    carousel.preview = JSON.parse(res.data.data);
    carousel.input = JSON.stringify(carousel.preview, null, 2);
  })
}

function Submit() {
  http.post("/variables", {
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
      <n-carousel autoplay show-arrow style="border-radius:11px;">
        <img v-for="i in carousel.preview" @click="OpenLink(i['url'])" :src="i['img']"
          style="width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;"
          :style="{ 'cursor': i['url'] ? 'pointer' : 'auto' }">
      </n-carousel>
      <n-input v-model:value="carousel.input" type="textarea" placeholder="JSON" rows="11" />
      <n-button @click="Add" block>添加</n-button>
      <n-button @click="Preview" block>预览</n-button>
      <n-button @click="Submit" block>提交</n-button>
    </n-space>
  </div>

</template>