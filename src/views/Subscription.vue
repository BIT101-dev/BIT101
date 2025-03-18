<!--
 * @Author: flwfdd
 * @Date: 2025-03-19 02:31:38
 * @LastEditTime: 2025-03-19 02:53:19
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import router from '@/router';
import http from '@/utils/request';
import { FormatTime, GetObjName, GetObjUrl } from '@/utils/tools';
import { SubscriptionLevel } from '@/utils/types';
import { onMounted, reactive } from 'vue';

interface Subscription {
  id: number;
  subscription_time: string;
  obj: string;
  level: SubscriptionLevel;
  text: string;
}

const subscriptions = reactive({
  page: 0,
  end: false,
  loading: false,
  list: [] as Subscription[],
})

const subscriptionLevels = {
  [SubscriptionLevel.None]: '取消订阅',
  [SubscriptionLevel.Silent]: '仅收藏',
  [SubscriptionLevel.Update]: '订阅更新',
  [SubscriptionLevel.Comment]: '订阅更新及评论',
}

function LoadSubscriptions() {
  if (subscriptions.loading || subscriptions.end) return;
  subscriptions.loading = true;
  http.get("/subscriptions", { params: { 'page': subscriptions.page } }).then(res => {
    if (res.data.length == 0) {
      subscriptions.end = true;
    } else {
      subscriptions.list = subscriptions.list.concat(res.data);
      subscriptions.page++;
    }
  }).finally(() => { subscriptions.loading = false; });
}

onMounted(() => {
  LoadSubscriptions();
})
</script>

<template>
  <div class="container">
    <n-card title="订阅 | Subscription">
    </n-card>

    <n-divider></n-divider>

    <n-card v-for="i in subscriptions.list" hoverable
      style="margin-bottom:11px;background-color: var(--card-bg-color);">
      <n-ellipsis :line-clamp="2" :tooltip="false" style="font-size:15px;">
        {{ GetObjName(i.obj) }}：{{ i.text }}
      </n-ellipsis>
      <n-space style="color:var(--text-color-3);font-size:14px;">
        {{ subscriptionLevels[i.level] }} 于 {{ FormatTime(i.subscription_time) }}
        <n-button v-if="i.obj" @click="router.push(GetObjUrl(i.obj))" text>查看></n-button>
      </n-space>
    </n-card>
    <n-divider style="color:var(--text-color-3);font-size:14px;">已加载{{ subscriptions.list.length }}条</n-divider>
    <n-button block @click="LoadSubscriptions()" :disabled="subscriptions.end" :loading="subscriptions.loading">
      {{ subscriptions.end ? '木有更多了' : '加载更多' }}</n-button>
    <n-divider></n-divider>
  </div>
</template>