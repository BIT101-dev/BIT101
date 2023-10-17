<!--
 * @Author: flwfdd
 * @Date: 2023-10-17 08:17:11
 * @LastEditTime: 2023-10-17 19:00:39
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import router from '@/router';
import http from '@/utils/request';
import { onMounted, reactive, watch } from 'vue';
import { useRoute } from 'vue-router';
import { SearchOutlined } from '@vicons/material';
import { Poster } from '@/utils/types';
import store from '@/utils/store';
import { FormatTime } from '@/utils/tools';

const gallery = reactive({
  search: "",
  order: "recommend",
  page: 0,
  end: false,
  loading: false,
  list: [] as Poster[]
})

function LoadPosters() {
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

const route = useRoute();
gallery.search = route.query.search as string;
onMounted(() => {
  LoadPosters();
})

function Search() {
  gallery.list = [];
  gallery.page = 0;
  gallery.end = false;
  LoadPosters();
}

function Refresh() {
  window.scrollTo(0, 0);
  gallery.list = [];
  gallery.page = 0;
  gallery.end = false;
  LoadPosters();
}

watch(() => gallery.order, () => {
  Search();
})

</script>

<template>
  <div class="container">
    <n-card title="话廊 | Gallery">
      <n-collapse default-expanded-names="search">
        <n-space vertical>
          <n-input-group>
            <n-input v-model:value="gallery.search" @keyup.enter="Search" placeholder="请输入关键词" maxlength="42"></n-input>
            <n-button type="default">搜索</n-button>
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

      <!-- <div style="display: flex;margin-top:10px;">
        <a :href="'/#/user/' + i.user.id" target="_blank" @click.stop="">
          <n-avatar round size-="x-small" :src="i.user.avatar + store.img_suffix" />
        </a>
        <span style="margin-left: 4px;margin-top:-6px">
          <div style="font-size: 16px;">{{ i.user.nickname }}</div>
          <div style="margin-top: -4px;font-size:14px;">{{ FormatTime(i.create_time) }}</div>
        </span>
      </div> -->

      <h3 style="margin:0;color:#0087A8;">{{ i.title }}</h3>

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

      <div
        style="color:#809BA8;font-size:14px;margin-top: 4px;display:flex;align-items:center;">
        <div style="display:flex;align-items: center;flex:1;">
          <a :href="'/#/user/' + i.user.id" target="_blank" @click.stop="" style="font-size:0;">
            <n-avatar round size="small" :src="i.user.avatar + store.img_suffix" />
          </a>
          <div style="width:2em;flex:1;">
            <n-ellipsis  style="margin-left:2px;">{{ i.user.nickname }}</n-ellipsis>
          </div>
        </div>
        <span>
          {{ i.like_num }}赞 | {{ i.comment_num }}评 | {{ FormatTime(i.create_time) }}
        </span>
      </div>
    </n-card>

    <n-divider style="color:#809BA8;font-size:14px;">已加载{{ gallery.list.length }}条</n-divider>

    <n-space vertical>
      <n-button block @click="LoadPosters()" :disabled="gallery.end" :loading="gallery.loading">
        {{ gallery.end ? '木有更多了' : '加载更多' }}
      </n-button>
      <n-button block @click="Refresh()" :loading="gallery.loading">
        刷新
      </n-button>
    </n-space>
  </div>
</template>