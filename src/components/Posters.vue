<!--
 * @Author: flwfdd
 * @Date: 2023-10-20 13:25:20
 * @LastEditTime: 2023-10-30 20:35:29
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import router from '@/router';
import http from '@/utils/request';
import { PropType, nextTick, onMounted, reactive, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { Poster } from '@/utils/types';
import { FormatTime, OpenLink } from '@/utils/tools';
import { ErrorOutlined } from '@vicons/material'
import Avatar from '@/components/Avatar.vue';
import store from '@/utils/store';
import ImageViewer from '@/components/ImageViewer/ImageViewer.vue';
import ImageBox from "@/components/ImageViewer/ImageBox.vue";
import { loadingBarRef } from '@/router';

export interface PostersStatus {
  mode: 'recommend' | 'search' | 'follow' | 'hot';
  search: string;
  order: 'similar' | 'new';
  uid: number;
}

const props = defineProps({
  value: {
    type: Object as PropType<PostersStatus>,
    required: true
  },
})

const posters = reactive({
  page: 0,
  end: false,
  loading: false,
  list: [] as Poster[],
  refresh_time: 0
})

function LoadPosters() {
  if (posters.loading || posters.end) return;
  
  posters.loading = true;
  loadingBarRef.value.start()
  
  let refresh_time = posters.refresh_time;
  http.get("/posters", {
    params: {
      mode: props.value.mode,
      page: posters.page,
      search: props.value.search,
      order: props.value.order,
      uid: props.value.uid
    }
  }).then(res => {
    loadingBarRef.value.finish()
    // 状态更新后可能之前的请求还没完成 得加上时间戳保证更新的是最新的
    if (refresh_time != posters.refresh_time) return;
    if (res.data.length == 0) posters.end = true;
    else {
      posters.list = posters.list.concat(res.data);
      posters.page++;
    }
    posters.loading = false;
  }).catch(() => { posters.loading = false; })
}

const load_more_observer = ref(null as any);
onMounted(async () => {
  await nextTick()
  loadingBarRef.value.start()
  LoadPosters();

  // 构建滚动观察器
  let observer = new IntersectionObserver(([entry]) => {
    if (posters.loading || posters.end) return;
    if (entry.isIntersecting) {
      LoadPosters();
    }
  });

  // 监听底部元素
  observer.observe(load_more_observer.value as Element);
})

watch(props, () => {
  posters.page = 0;
  posters.list = [];
  posters.loading = false;
  posters.end = false;
  posters.refresh_time++;
  LoadPosters();
})
</script>

<template>
  <n-card v-for="i in posters.list" @click="router.push('/gallery/' + i['id'])" hoverable
    style="margin-bottom:11px;cursor:pointer;">

    <div>
      <n-ellipsis :line-clamp="2" :tooltip="false" style="color:var(--gallery-posters-title-color);font-size:18px;font-weight:bold;margin:0;">{{ i.title }}</n-ellipsis>
    </div>

    <n-space v-if="i.claim.id != 0 || i.public == false">
      <n-tag v-if="i.public == false" round :bordered="false" type="warning" size="small">
        仅自己可见
        <template #icon>
          <n-icon :component="ErrorOutlined" />
        </template>
      </n-tag>
      <n-tag v-if="i.claim.id != 0" round :bordered="false" type="error" size="small">
        {{ i.claim.text }}
        <template #icon>
          <n-icon :component="ErrorOutlined" />
        </template>
      </n-tag>
      <br />
    </n-space>

    <n-ellipsis :line-clamp="2" :tooltip="false">{{ i.text.substring(0,2333) }}</n-ellipsis>

    <ImageViewer v-if="i.images.length" :images="i.images" />

    <div style="color:#809BA8;font-size:14px;margin-top: 11px;display:flex;align-items:center;">
      <div @click="OpenLink('/user/' + i.user.id)" @click.stop=""
        style="display:flex;align-items: center;flex:1;">
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

  <n-divider style="color:#809BA8;font-size:14px;">已加载{{ posters.list.length }}条</n-divider>

  <n-button block @click="LoadPosters()" :disabled="posters.end || posters.loading" :loading="posters.loading">
    {{ posters.end ? '去做点更有意思的事情吧' : '加载更多' }}
  </n-button>
</template>