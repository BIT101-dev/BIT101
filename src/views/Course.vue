<!--
 * @Author: flwfdd
 * @Date: 2022-07-29 21:21:21
 * @LastEditTime: 2025-03-19 02:14:39
 * @Description: 
 * _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import { onMounted, reactive } from 'vue';
import { useRoute } from 'vue-router';

const course = reactive({
  search: "",
  order: "new",
  page: 0,
  end: false,
  loading: false,
  list: [],
})

function LoadCourses() {
  course.loading = true;
  http.get("/courses", {
    params: {
      search: course.search,
      order: course.order,
      page: course.page,
    }
  }).then(res => {
    if (res.data.length == 0) course.end = true;
    else {
      course.list = course.list.concat(res.data);
      course.page++;
    }
    course.loading = false;
  }).catch(() => { course.loading = false; })
}

const route = useRoute();
course.search = route.query.search as string;
onMounted(() => {

  LoadCourses();
})

function Search() {
  course.list = [];
  course.page = 0;
  course.end = false;
  LoadCourses();
}

</script>

<template>
  <div class="container">
    <n-card title="课程 | Course">
      <n-collapse default-expanded-names="search">
        <n-collapse-item title="课程检索" name="search">
          <n-space vertical>
            <div>搜索</div>
            <n-input v-model:value="course.search" @keyup.enter="Search" placeholder="请输入关键词" maxlength="42"></n-input>
            <div>排序方式</div>
            <n-radio-group v-model:value="course.order" name="排序方式">
              <n-space>
                <n-radio value="new">最新</n-radio>
                <n-radio value="rate">最高分</n-radio>
                <n-radio value="like">最多赞</n-radio>
                <n-radio value="comment">最多评</n-radio>
              </n-space>
            </n-radio-group>
            <n-button @click="Search" ghost block>检索</n-button>
            <div v-if="course.search && course.order != 'search'" style="font-size:14px;color:var(--text-color-3);">
              结果不准确？试试相关搜索</div>
          </n-space>
        </n-collapse-item>
      </n-collapse>
    </n-card>

    <n-divider></n-divider>

    <router-link v-for="i in course.list" :to="'/course/' + i['id']" style="text-decoration: none;">
      <n-card hoverable style="margin-bottom:11px;cursor:pointer;">
        <h3 style="margin:0;color:var(--text-color-1);">{{ i['name'] }}</h3>
        <n-rate :value="i['rate'] / 2" allow-half readonly />
        <div>授课教师：{{ i['teachers_name'] }}</div>
        <div style="color:var(--text-color-3);font-size:14px;">{{ i['like_num'] }}赞 | {{ i['comment_num'] }}评价 | {{
          (i['rate'] /
            2).toFixed(2)
        }}分</div>
      </n-card>
    </router-link>
    <n-divider style="color:var(--text-color-3);font-size:14px;">已加载{{ course.list.length }}条</n-divider>
    <n-button block @click="LoadCourses()" :disabled="course.end" :loading="course.loading">
      {{ course.end ? '木有更多了' : '加载更多' }}</n-button>
  </div>
</template>