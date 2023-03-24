<script setup lang="ts">
import http from '@/utils/request';
import { Clip, setTitle } from '@/utils/tools';
import { onMounted, reactive } from 'vue';
import { useRoute } from 'vue-router';
import { ThumbUpOutlined, ThumbUpFilled, ShareOutlined } from '@vicons/material';
import Comment from '@/components/Comment.vue';
import router from '@/router';

const course = reactive({
  id: "",
  comment_num: 0,
  like_num: 0,
  name: "",
  number: "",
  rate_sum: 0,
  rate: 0,
  teachers: [] as any[],
  like: false,
  like_loading: false,
})


function Like() {
  course.like_loading = true;
  http.post("/reaction/like", { 'obj': 'course' + course.id })
    .then(res => {
      course.like = res.data.like;
      course.like_num = res.data.like_num;
      course.like_loading = false;
    }).catch(() => { course.like_loading = false; })
}

function ClipUrl() {
  Clip(window.location.href, "课程链接已复制OvO");
}

function Open(url: string) {
  window.open(url, '_blank');
}

function LoadCourse() {
  return http.get('/courses/' + course.id).then(res => {
    let data = res.data;
    course.comment_num = data.comment_num;
    course.like_num = data.like_num;
    course.name = data.name;
    course.number = data.number;
    course.rate_sum = data.rate_sum;
    course.rate = data.rate / 2;
    course.like = data.like;
    let names = data.teachers_name.split(',');
    let numbers = data.teachers_number.split(',');
    for (let i in names) course.teachers.push({ 'name': names[i], 'number': numbers[i] })
  })
}

const route = useRoute();
course.id = route.params.id as string;
onMounted(async () => {
  await LoadCourse()
  const teachers_names = course.teachers.map(t => t.name)
  setTitle(`${course.name}（${teachers_names.join('、')}）`, '课程')
})

</script>

<template>
  <div class="container">
    <h1 style="color:#00BCD4;margin-bottom: 0px;">{{ course.name }}</h1>

    <span style="display:flex;">
      <n-rate :value="course.rate" allow-half size="large" readonly />
      <span style="margin-left:4px;color:#999;">{{ course.rate.toFixed(2) }}分（{{ course.comment_num }}人评价）</span>
    </span>
    <div style="color:#999;font-size:12px;">课程编号：{{ course.number }}</div>
    <br />
    <n-space vertical>


      <n-space>
        授课教师：
        <router-link :to="'/course/?search=' + i['number']" v-for="(i, ind) in course.teachers"
          style="text-decoration:none;color:#FF8533">
          {{ i['name'] }}</router-link>
      </n-space>
      <router-link :to="'/course/?search=' + course.number" style="text-decoration:none;color:#FF8533">查找其他老师讲授的该课程
      </router-link>

      <n-space style="margin-top:4px">
        <n-button @click="Like" icon-placement="right" color="#fb7299" :ghost="!course.like"
          :loading="course.like_loading" :disabled="course.like_loading">
          <template #icon>
            <n-icon>
              <ThumbUpFilled v-if="course.like" />
              <ThumbUpOutlined v-else />
            </n-icon>
          </template>
          {{ course.like_num }}人点赞
        </n-button>
        <n-button @click="ClipUrl" icon-placement="right" ghost>
          <template #icon>
            <n-icon>
              <ShareOutlined />
            </n-icon>
          </template>
          分享
        </n-button>
        <n-button @click="Open(`https://onedrive.bit101.cn/zh-CN/教学大纲/${course.name}-${course.number}/`)" ghost>
          查看教学大纲
        </n-button>
        <n-button @click="Open(`https://onedrive.bit101.cn/zh-CN/course/${course.name}-${course.number}`)" ghost>
          查看课程资料
        </n-button>
        <n-button @click="router.push('/course/upload/' + course.id)" ghost>
          上传课程资料
        </n-button>
      </n-space>
    </n-space>
    <n-divider style="color:#809BA8;font-size:14px;">我的评价是</n-divider>
    <n-alert closable :show-icon="false" style="margin-bottom:11px;">
      <div style="font-size:14px;">评分请尽量客观，以授课质量为主要视角<br />可以谈谈上课风格、给分方式、作业情况、学习感想等</div>
    </n-alert>
    <Comment :obj='"course" + course.id' :rate="true"></Comment>
    <br />
  </div>
</template>