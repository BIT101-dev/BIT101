<script setup lang="ts">
import http from '@/utils/request';
import { Clip, OpenLink, Share, setTitle } from '@/utils/tools';
import { computed, onMounted, reactive } from 'vue';
import { useRoute } from 'vue-router';
import { ThumbUpOutlined, ThumbUpFilled, ShareOutlined } from '@vicons/material';
import Comment from '@/components/Comment.vue';
import router from '@/router';

// 引入 ECharts
import VChart from 'vue-echarts';
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import {
  TooltipComponent,
  DataZoomComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

use([
  TooltipComponent,
  DataZoomComponent,
  LegendComponent,
  GridComponent,
  LineChart,
  CanvasRenderer
])



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

// 课程历史
const history = reactive({
  show: false,
  loading: true,
  terms: [] as any[],
  avg_scores: [] as any[],
  max_scores: [] as any[],
  student_nums: [] as any[],
})

function GetCourseHistory() {
  history.loading = true;
  if (!course.number) return;
  history.show = true;
  http.get('/courses/histories/' + course.number)
    .then(res => {
      let data = res.data;
      // 根据学期排序
      data.sort((a: any, b: any) => a.term.localeCompare(b.term));
      // 填入数据
      history.terms = [];
      history.avg_scores = [];
      history.max_scores = [];
      history.student_nums = [];
      for (let i of data) {
        history.terms.push(i.term);
        history.avg_scores.push(i.avg_score);
        history.max_scores.push(i.max_score);
        history.student_nums.push(i.student_num);
      }
      if (!history.terms.length) {
        window.$message.error("没有历史数据Orz");
        history.show = false;
      } else {
        history.loading = false;
      }
    }).catch(() => {
      history.loading = false;
      history.show = false;
    })
}

const option = computed(() => {
  return {
    tooltip: {
      trigger: 'axis'
    },
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100
      },
      {
        start: 0,
        end: 100
      }
    ],
    legend: {
      data: ['平均分', '最高分', '学习人数']
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: history.terms
    },
    yAxis: [
      {
        name: '分数',
        type: 'value'
      },
      {
        name: '人数',
        type: 'value'
      }
    ],
    series: [
      {
        name: '平均分',
        type: 'line',
        yAxisIndex: 0,
        data: history.avg_scores
      },
      {
        name: '最高分',
        type: 'line',
        yAxisIndex: 0,
        data: history.max_scores
      },
      {
        name: '学习人数',
        type: 'line',
        yAxisIndex: 1,
        data: history.student_nums
      },
    ]
  }
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

function ShareCourse() {
  let teachers_names = course.teachers.map(t => t.name);
  let title='BIT101课程｜'+`${course.name}（${teachers_names.join(' ')}）`;
  Share(title, title, window.location.href);
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
          style="text-decoration:none;color:var(--primary)">
          {{ i['name'] }}</router-link>
      </n-space>
      <router-link :to="'/course/?search=' + course.number" style="text-decoration:none;color:var(--primary)">查找其他老师讲授的该课程
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
        <n-button @click="ShareCourse" icon-placement="right" ghost>
          <template #icon>
            <n-icon>
              <ShareOutlined />
            </n-icon>
          </template>
          分享
        </n-button>
        <n-button @click="OpenLink(`https://onedrive.bit101.cn/zh-CN/教学大纲/${course.name}-${course.number}/`)" ghost>
          教学大纲
        </n-button>
        <n-button @click="OpenLink(`https://onedrive.bit101.cn/zh-CN/course/${course.name}-${course.number}`)" ghost>
          共享资料
        </n-button>
        <n-button @click="router.push('/course/upload/' + course.id)" ghost>
          上传资料
        </n-button>
        <n-button @click="GetCourseHistory" ghost>
          历史记录
        </n-button>
      </n-space>
    </n-space>
    <n-divider style="color:#809BA8;font-size:14px;">我的评价是</n-divider>
    <n-alert closable :show-icon="false" style="margin-bottom:11px;">
      <div style="font-size:14px;">评分请尽量客观，以授课质量为主要视角<br />可以谈谈上课风格、给分方式、作业情况、学习感想等</div>
    </n-alert>
    <Comment :obj='"course" + course.id' :rate="true"></Comment>
    <br />

    <n-modal v-model:show="history.show" preset="card" style="width:624px" title="课程历史">
      <n-spin v-if="history.loading" size="large" style="width:100%;text-align: center;" />
      <div v-else>
        <v-chart :option="option" style="height: 42vh;" autoresize />
        <p style="font-size: small;">
          注：数据仅供参考，不区分教学班。<br/>
          「如果一个人把政策评分作为自己的至高追求，那么他就是这个政策的牺牲品。」
          <div style="text-align: right;">——《上海交通大学生存手册》</div>
        </p>
      </div>
    </n-modal>
  </div>
</template>