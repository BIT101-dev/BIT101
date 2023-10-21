<!--
 * @Author: flwfdd
 * @Date: 2023-10-17 08:17:11
 * @LastEditTime: 2023-10-20 21:26:51
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import router from '@/router';
import http from '@/utils/request';
import { Teleport, onMounted, reactive, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { Poster } from '@/utils/types';
import { FormatTime, OpenLink } from '@/utils/tools';
import { ErrorOutlined, RefreshRound, AddRound } from '@vicons/material'
import Posters, { PostersStatus } from '@/components/Posters.vue';

const posters = ref({
  mode: 'recommend',
  search: "",
  order: "like",
  uid: -1
} as PostersStatus
);

const gallery = reactive({
  tab: "recommend",
  search: "",
  order: "recommend",
})

function Load(force = false) {
  if (gallery.tab == "follow") {
    posters.value.mode = "follow";
  } else if (gallery.tab == "recommend") {
    posters.value.mode = gallery.search ? "search" : "recommend";
    posters.value.search = gallery.search;
    posters.value.order = gallery.order == "new" ? "new" : "like";
  } else if (gallery.tab == "hot") {
    posters.value.mode = "hot";
  }
  if (force) posters.value = JSON.parse(JSON.stringify(posters.value));
}


function Refresh() {
  window.scrollTo(0, 0);
  Load(true);
}

watch(() => [gallery.tab, gallery.order], () => {
  Load();
})

</script>

<template>
  <div class="container">
    <div style="text-align:center;">
      <h2 style="color:#00BCD4">话廊 | Gallery</h2>
    </div>

    <n-divider></n-divider>

    <n-tabs type="segment" v-model:value="gallery.tab">
      <n-tab-pane name="follow" tab="关注">
      </n-tab-pane>
      <n-tab-pane name="recommend" tab="推荐">
        <n-space vertical style="margin-bottom: 11px;">
          <n-input-group>
            <n-input v-model:value="gallery.search" @keyup.enter="Refresh" placeholder="请输入关键词" maxlength="42"></n-input>
            <n-button type="default" @click="Refresh">搜索</n-button>
          </n-input-group>
          <n-radio-group v-model:value="gallery.order">
            <n-space>
              <n-radio value="recommend">推荐</n-radio>
              <n-radio value="new">最新</n-radio>
            </n-space>
          </n-radio-group>
        </n-space>
      </n-tab-pane>

      <n-tab-pane name="hot" tab="热榜">
      </n-tab-pane>
    </n-tabs>

    <Posters :value="posters" />

    <n-space vertical style="position:fixed;right:4.2vw;bottom:4.2vw;">
      <n-button @click="Refresh()" circle :bordered="false"
        style="background-color:#FFFA;width:50px;height: 50px;box-shadow: 0 0 11px #ccc;">
        <template #icon>
          <n-icon :component="RefreshRound" size="24" />
        </template>
      </n-button>
      <n-button @click="OpenLink('/#/gallery/edit/0')" circle :bordered="false"
        style="background-color:#FFFA;width:50px;height: 50px;box-shadow: 0 0 11px #ccc;">
        <template #icon>
          <n-icon :component="AddRound" size="24" />
        </template>
      </n-button>
    </n-space>

  </div>
</template>