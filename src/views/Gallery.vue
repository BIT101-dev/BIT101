<!--
 * @Author: flwfdd
 * @Date: 2023-10-17 08:17:11
 * @LastEditTime: 2025-03-18 18:47:40
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import { onMounted, reactive, ref, watch } from 'vue';
import { OpenLink, opacityColor } from '@/utils/tools';
import RefreshRound from '@vicons/material/RefreshRound'
import AddRound from '@vicons/material/AddRound'
import Posters, { PostersStatus } from '@/components/Posters.vue';
import { useThemeVars } from 'naive-ui';

const themeVars = useThemeVars();

const posters = ref({
  mode: 'recommend',
  search: "",
  order: "new",
  uid: -1
} as PostersStatus
);

const gallery = reactive({
  tab: "recommend",
  search: "",
  order: "new",
})

function Load(force = false) {
  if (gallery.tab == "follow") {
    posters.value.mode = "follow";
    posters.value.search = "";
    posters.value.order = "new";
  } else if (gallery.tab == "new") {
    posters.value.mode = "search";
    posters.value.search = "";
    posters.value.order = "new";
  } else if (gallery.tab == "recommend") {
    posters.value.mode = "recommend";
  } else if (gallery.tab == "hot") {
    posters.value.mode = "hot";
  } else if (gallery.tab == "search") {
    posters.value.mode = "search";
    posters.value.search = gallery.search;
    posters.value.order = gallery.order == "like" ? "like" : gallery.order == "comment" ? "comment" : "new";
  }
  if (force) posters.value = JSON.parse(JSON.stringify(posters.value));
}

// 轮播图
const carousel_data = ref([])
function LoadCarousel() {
  http.get("/variables?obj=gallery_carousel").then((res) => {
    carousel_data.value = JSON.parse(res.data.data);
  })
}

function Refresh() {
  window.scrollTo(0, 0);
  Load(true);
}

watch(() => [gallery.tab, gallery.order], () => {
  Load();
})

onMounted(() => {
  LoadCarousel();
})

</script>

<template>
  <div class="container">
    <div style="text-align:center;">
      <n-h2 style="margin:4px;">话廊 | Gallery</n-h2>
      <n-carousel v-if="carousel_data.length" autoplay show-arrow style="border-radius:11px;margin-bottom:4px;">
        <img v-for="i in carousel_data" @click="OpenLink(i['url'])" :src="i['img']"
          style="width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;"
          :style="{ 'cursor': i['url'] ? 'pointer' : 'auto' }">
      </n-carousel>
    </div>

    <n-tabs type="segment" v-model:value="gallery.tab">
      <n-tab-pane name="follow" tab="关注">
      </n-tab-pane>

      <n-tab-pane name="new" tab="最新">
      </n-tab-pane>

      <n-tab-pane name="recommend" tab="推荐">
      </n-tab-pane>

      <n-tab-pane name="hot" tab="热门">
      </n-tab-pane>

      <n-tab-pane name="search" tab="搜索">
        <n-space vertical style="margin-bottom: 11px;">
          <n-input-group>
            <n-input v-model:value="gallery.search" @keyup.enter="Refresh" placeholder="请输入关键词"
              maxlength="42"></n-input>
            <n-button type="default" @click="Refresh">搜索</n-button>
          </n-input-group>
          <n-radio-group v-model:value="gallery.order">
            <n-space>
              <n-radio value="new">最新</n-radio>
              <n-radio value="like">最多赞</n-radio>
              <n-radio value="comment">最多评</n-radio>
            </n-space>
          </n-radio-group>
        </n-space>
      </n-tab-pane>
    </n-tabs>

    <Posters :value="posters" />

    <n-space vertical style="position:fixed;right:4.2vw;bottom:4.2vw;">
      <n-button @click="Refresh()" circle :bordered="false"
        :style="{ 'background-color': opacityColor(themeVars.baseColor, 0.84), 'width': '50px', 'height': '50px', 'box-shadow': '0 0 11px #CCCCCCCC' }">
        <template #icon>
          <n-icon :component="RefreshRound" size="24" />
        </template>
      </n-button>
      <n-button @click="OpenLink('/gallery/edit/0')" circle :bordered="false"
        :style="{ 'background-color': opacityColor(themeVars.baseColor, 0.84), 'width': '50px', 'height': '50px', 'box-shadow': '0 0 11px #CCCCCCCC' }">
        <template #icon>
          <n-icon :component="AddRound" size="24" />
        </template>
      </n-button>
    </n-space>

  </div>
</template>