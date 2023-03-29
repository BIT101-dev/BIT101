<!--
 * @Author: flwfdd
 * @Date: 2022-07-31 22:43:32
 * @LastEditTime: 2023-03-25 15:44:39
 * @Description: 
 * _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import { onMounted, reactive, ref } from 'vue';
import Billboard from '@/components/Billboard.vue';


const billboard_item_template = {
  "title": "",
  "text":"",
  "url": "",
  "img":"",
}

const billboard = reactive({
  input: "",
  preview: [],
})

function Add() {
  let x = JSON.parse(billboard.input);
  x.push(billboard_item_template);
  billboard.input = JSON.stringify(x, null, 2);
}

function Preview() {
  billboard.preview=JSON.parse(billboard.input);
}

function Load() {
  http.get("/variables?obj=billboard").then((res) => {
    billboard.preview = JSON.parse(res.data.data);
    billboard.input = JSON.stringify(billboard.preview, null, 2);
  })
}

function Submit() {
  http.post("/variables", {
    obj: 'billboard',
    data: JSON.stringify(billboard.preview),
  })
}

onMounted(() => { Load() })

</script>

<template>
  <div class="container">
    <n-space vertical>
      <h2>橱窗设置</h2>
      <Billboard :data="billboard.preview"></Billboard>
      <n-input v-model:value="billboard.input" type="textarea" placeholder="JSON" rows="11" />
      <n-button @click="Add" block>添加</n-button>
      <n-button @click="Preview" block>预览</n-button>
      <n-button @click="Submit" block>提交</n-button>
    </n-space>
  </div>

</template>