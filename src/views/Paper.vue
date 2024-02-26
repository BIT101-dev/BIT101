<!--
 * @Author: flwfdd
 * @Date: 2022-07-27 17:09:21
 * @LastEditTime: 2024-02-26 17:00:47
 * @Description: 
 * _(:з」∠)_
-->
<script setup lang="ts">
import router from '@/router';
import http from '@/utils/request';
import { FormatTime } from '@/utils/tools';
import { onMounted, reactive } from 'vue';

const papers = reactive({
  search: "",
  order: "new",
  page: 0,
  end: false,
  loading: false,
  list: [],
})

function LoadPapers() {
  papers.loading = true;
  http.get("/papers", {
    params: {
      search: papers.search,
      order: papers.order,
      page: papers.page,
    }
  }).then(res => {
    if (res.data.length == 0) papers.end = true;
    else {
      papers.list = papers.list.concat(res.data);
      if (papers.order != 'rand') papers.page++;
    }
    papers.loading = false;
  }).catch(() => { papers.loading = false; })
}

onMounted(() => {
  LoadPapers();
})

function Search() {
  papers.list = [];
  papers.page = 0;
  papers.end = false;
  LoadPapers();
}

</script>

<template>
  <div class="container">
    <n-card title="文章 | Paper">
      <n-button @click="router.push('/paper/edit/0')" type="success" ghost style="margin-bottom:4px;margin-top: -11px;"
        block>新建 Paper</n-button>
      <n-collapse default-expanded-names="search">
        <n-collapse-item title="Paper检索" name="search">
          <n-space vertical>
            <div>搜索</div>
            <n-input v-model:value="papers.search" @keyup.enter="Search" placeholder="请输入关键词" maxlength="42"></n-input>
            <n-radio-group v-model:value="papers.order" name="排序方式">
              <n-space>
                排序方式
                <n-radio value="new"> 最新</n-radio>
                <n-radio value="rand"> 随机</n-radio>
                <n-radio value="like"> 赞数</n-radio>
              </n-space>
            </n-radio-group>
            <n-button @click="Search" ghost block>检索</n-button>
          </n-space>
        </n-collapse-item>
      </n-collapse>
    </n-card>

    <n-divider></n-divider>

    <router-link v-for="i in papers.list" :to="'/paper/' + i['id']" style="text-decoration: none;">
      <n-card hoverable style="margin-bottom:11px;cursor:pointer;">
        <h3 style="margin:0;color:var(--text-color-1);">{{ i['title'] }}</h3>
        <n-ellipsis :line-clamp="2" :tooltip="false" style="font-size:15px;">
          {{ i['intro'] }}
        </n-ellipsis>
        <div style="color:var(--text-color-3);font-size:14px;">{{ i['like_num'] }}赞 | {{ i['comment_num'] }}评论 |
          {{ FormatTime(i['update_time']) }}更新</div>
      </n-card>
    </router-link>
    <n-divider style="color:var(--text-color-3);font-size:14px;">已加载{{ papers.list.length }}条</n-divider>
    <n-button block @click="LoadPapers()" :disabled="papers.end" :loading="papers.loading">
      {{ papers.end ? '木有更多了' : '加载更多' }}</n-button>
  </div>
</template>