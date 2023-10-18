<!--
 * @Author: flwfdd
 * @Date: 2023-10-17 08:17:11
 * @LastEditTime: 2023-10-18 14:08:43
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
import Avatar from '@/components/Avatar.vue';

const gallery = reactive({
  search: "",
  order: "recommend",
  page: 0,
  end: false,
  loading: false,
  list: [] as Poster[]
})

function LoadPosters() {
  if(gallery.loading||gallery.end)return;
  gallery.loading = true;
  http.get("/posters", {
    params: {
      search: gallery.search,
      order: gallery.order,
      page: gallery.page,
      uid: -1
    }
  }).then(res => {
    if (res.data.length == 0) gallery.end = true;
    else {
      gallery.list = gallery.list.concat(res.data);
      gallery.page++;
    }
    gallery.loading = false;
  }).catch(() => { gallery.loading = false; })
}

function Search() {
  gallery.list = [];
  gallery.page = 0;
  gallery.end = false;
  LoadPosters();
}

function Refresh() {
  window.scrollTo(0, 0);
  Search();
}

watch(() => gallery.order, () => {
  Search();
})

const route = useRoute();
gallery.search = route.query.search as string;
const load_more_observer = ref(null as any);
onMounted(() => {
  LoadPosters();

  // 构建滚动观察器
  let observer = new IntersectionObserver(([entry]) => {
    if(gallery.loading||gallery.end)return;
    if (entry.isIntersecting) {
      LoadPosters();
    }
  });

  // 监听底部元素
  observer.observe(load_more_observer.value as Element);
})
</script>

<template>
  <div class="container">
    <n-card title="话廊 | Gallery">
      <n-collapse default-expanded-names="search">
        <n-space vertical>
          <n-input-group>
            <n-input v-model:value="gallery.search" @keyup.enter="Search" placeholder="请输入关键词" maxlength="42"></n-input>
            <n-button type="default" @click="Search">搜索</n-button>
          </n-input-group>
          <n-radio-group v-model:value="gallery.order">
            <n-space>
              <n-radio value="recommend">推荐</n-radio>
              <n-radio value="new">最新</n-radio>
            </n-space>
          </n-radio-group>
        </n-space>
      </n-collapse>
    </n-card>

    <n-divider></n-divider>

    <n-card v-for="i in gallery.list" @click="router.push('/gallery/' + i['id'])" hoverable
      style="margin-bottom:11px;cursor:pointer;">

      <h3 style="margin:0;color:#0087A8;">{{ i.title }}</h3>

      <n-tag v-if="i.claim" round :bordered="false" type="error" size="small">
        {{ i.claim }}
        <template #icon>
          <n-icon :component="ErrorOutlined" />
        </template>
      </n-tag>

      <n-ellipsis :line-clamp="2" :tooltip="false">{{ i.text }}</n-ellipsis>
      <n-image-group>
        <n-grid x-gap="5" y-gap="5" :cols="3" style="max-width: 424px;">
          <n-gi v-for="(image, idx) in i.images" v-show="idx <= 2">
            <div @click.stop="" style="height:0;padding-bottom:100%;position:relative;">
              <n-image :src="image" object-fit="cover"
                style="width:100%;height:100%;position:absolute;top:0;left:0;border-radius: 5%;"
                :img-props="{ 'style': 'width:100%;' }" />
              <div v-if="idx == 2 && i.images.length > 3"
                style="width:100%;height:100%;position:absolute;border-radius:5%;background-color:rgba(0,0,0,0.5);display:flex;justify-content:center;align-items:center;pointer-events:none;">
                <h2 style="color:#fff">+{{ i.images.length - 3 }}</h2>
              </div>
            </div>
          </n-gi>
        </n-grid>
      </n-image-group>

      <div style="color:#809BA8;font-size:14px;margin-top: 11px;display:flex;align-items:center;">
        <div @click="OpenLink('/#/user/' + i.user.id,true)" @click.stop="" style="display:flex;align-items: center;flex:1;">
          <Avatar :user="i.user" :size="24" round />

          <div style="width:2em;flex:1;">
            <n-ellipsis style="margin-left:2px;">{{ i.user.nickname }}</n-ellipsis>
          </div>
        </div>
        <span>
          {{ i.like_num }}赞 | {{ i.comment_num }}评 | {{ FormatTime(i.create_time) }}
        </span>
      </div>
    </n-card>

    <div ref="load_more_observer"></div>

    <n-divider style="color:#809BA8;font-size:14px;">已加载{{ gallery.list.length }}条</n-divider>

    <n-button block @click="LoadPosters()" :disabled="gallery.end" :loading="gallery.loading">
      {{ gallery.end ? '木有更多了' : '加载更多' }}
    </n-button>

    <Teleport to="body">
      <n-space vertical style="position:fixed;right:4.2vw;bottom:4.2vw;">
        <n-button @click="Refresh()" circle :bordered="false"
          style="background-color:#FFFA;width:50px;height: 50px;box-shadow: 0 0 11px #ccc;">
          <template #icon>
            <n-icon :component="RefreshRound" size="24" />
          </template>
        </n-button>
        <n-button @click="Refresh()" circle :bordered="false"
          style="background-color:#FFFA;width:50px;height: 50px;box-shadow: 0 0 11px #ccc;">
          <template #icon>
            <n-icon :component="AddRound" size="24" />
          </template>
        </n-button>
      </n-space>

    </Teleport>
  </div>
</template>