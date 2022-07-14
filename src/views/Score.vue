<!--
 * @Author: flwfdd
 * @Date: 2022-06-26 18:52:08
 * @LastEditTime: 2022-07-12 01:30:47
 * @Description: 
 * _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import { WebvpnVerify, webvpn } from '@/utils/tools';
import { reactive, ref, onMounted, watch } from 'vue';

const user = reactive({
  sid: "",
  password: ""
})

//排序函数
function CustomSorter(k: string) {
  return (a: any, b: any) => {
    if (!a[k] || !b[k]) return 1;
    if (!isNaN(a[k])) {
      return a[k] - b[k];
    } else if (a[k].search("%") != -1) {
      return parseInt(a[k]) - parseInt(b[k]);
    } else {
      return a[k] < b[k] ? -1 : 1;
    }
  }
}

const columns = [
  {
    title: '课程名称',
    key: '课程名称',
    fixed: 'left',
    width: 99,
    sorter: 'default',
  },
  {
    title: '成绩',
    key: '成绩',
    width: 66,
    sorter: CustomSorter('成绩'),
  },
  {
    title: '平均分',
    key: '平均分',
    width: 88,
    sorter: CustomSorter('平均分'),
  },
  {
    title: '学分',
    key: '学分',
    width: 66,
    sorter: CustomSorter('学分'),
  },
  {
    title: '班级排名',
    key: '本人成绩在班级中占',
    width: 99,
    sorter: CustomSorter('本人成绩在班级中占'),
  },
  {
    title: '专业排名',
    key: '本人成绩在专业中占',
    width: 99,
    sorter: CustomSorter('本人成绩在专业中占'),
  },
  {
    title: '开课学期',
    key: '开课学期',
    width: 99,
    sorter: 'default',
  },
  {
    title: '课程性质',
    key: '课程性质',
    width: 99,
    sorter: 'default',
  },
]

const ori_data = ref([] as any);
const data = ref([] as any);
const loading = ref(false);
const detail = ref(false);
const search = ref("");
const course_type = reactive({
  "list": [] as any,
  "filter": [] as any,
});
const course_time = reactive({
  "list": [] as any,
  "filter": [] as any,
});
const stat = reactive({
  credit: 0,
  num: 0,
  score: "",
  gpa: "",
  avg_score: "",
  avg_gpa: "",
})

function Score2Num(s: string) {
  let ind = ["优秀", "良好", "中等", "及格", "不及格"].indexOf(s);
  if (ind != -1) return [95, 85, 75, 65, 0][ind];
  return Number(s);
}

function Score2GPA(s: string) {
  let ind = ["优秀", "良好", "中等", "及格", "不及格"].indexOf(s);
  if (ind != -1) return [4.0, 3.6, 2.8, 1.7, 0][ind];
  let x = Number(s);
  if (x < 60) return 0;
  return 4 - (3 * (100 - x) * (100 - x)) / 1600;
}

function Filter() {
  let credit_sum = 0;
  let score_sum = 0;
  let gpa_sum = 0;
  let avg_score_sum = 0;
  let avg_gpa_sum = 0;
  data.value = [];
  stat.num = 0;
  for (let i of ori_data.value) {
    if (
      i["课程名称"].search(search.value) != -1 &&
      course_type.filter.indexOf(i["课程性质"]) != -1 &&
      course_time.filter.indexOf(i["开课学期"]) != -1
    ) {
      let credit = Number(i["学分"]);
      stat.num++;
      data.value.push(i);
      if (isNaN(credit) || credit == 0) continue;
      let score = Score2Num(i["成绩"]);
      let avg_score = Score2Num(i["平均分"]);
      let gpa = Score2GPA(i["成绩"]);
      let avg_gpa = Score2GPA(i["平均分"]);
      credit_sum += credit;
      score_sum += score * credit;
      gpa_sum += gpa * credit;
      avg_score_sum += avg_score * credit;
      avg_gpa_sum += avg_gpa * credit;
    }
  }
  stat.credit = credit_sum;
  stat.score = (score_sum / credit_sum).toFixed(4);
  stat.avg_score = (avg_score_sum / credit_sum).toFixed(4);
  stat.gpa = (gpa_sum / credit_sum).toFixed(4);
  stat.avg_gpa = (avg_gpa_sum / credit_sum).toFixed(4);
}

function GetList() {
  if (!webvpn.cookie) return;
  loading.value = true;
  http
    .get("/score/", {
      params: {
        cookie: webvpn.cookie,
        detail: detail.value ? true : '',
      },
    })
    .then((res) => {
      loading.value = false;
      let ori_table = res.data.data;
      let ori_head = ori_table[0];
      ori_data.value = [];
      for (let i = 1; i < ori_table.length; i++) {
        let row = {};
        for (let j in ori_table[i]) {
          row[ori_head[j]] = ori_table[i][j];
        }
        ori_data.value.push(row);
      }
      let s;
      let course_type_tmp = [];
      let course_time_tmp = [];
      course_type.list = [];
      course_time.list = [];
      for (let i of ori_data.value) {
        s = i["课程性质"];
        if (course_type_tmp.indexOf(s) == -1) {
          course_type_tmp.push(s);
          course_type.list.push({ label: s, value: s });
        }

        s = i["开课学期"];
        if (course_time_tmp.indexOf(s) == -1) {
          course_time_tmp.push(s);
          course_time.list.push({ label: s, value: s });
        }

      }
      course_type.filter = course_type_tmp.concat();
      course_time.filter = course_time_tmp.concat();
      Filter();
    })
}

const modal = ref(false);
const modal_data = ref({});
function RowProps(row: any) {
  return {
    style: 'cursor: pointer;',
    onClick: () => {
      modal_data.value = row;
      modal.value = true;
    }
  }
}

onMounted(() => {
  GetList();
})

watch(() => webvpn.cookie, () => {
  GetList();
})

</script>

<template>
  <div class="container">
    <n-card title="成寄查询">
      <n-space vertical v-if="!webvpn.cookie">
        <n-input v-model:value="user.sid" type="number" placeholder="学号" />
        <n-input v-model:value="user.password" type="password" show-password-on="click"
          placeholder="学校统一身份认证密码" />
        <n-button @click="WebvpnVerify(user.sid, user.password)"
          :disabled="!user.sid || !user.password || webvpn.loading" block :loading="webvpn.loading">
          查询
        </n-button>
      </n-space>
      <n-space vertical v-else>
        <n-button v-show="!detail" @click="detail = true, GetList()" :disabled="loading || detail" block>
          查询详细信息（较慢）
        </n-button>
        <n-select v-model:value="course_type.filter" multiple :options="course_type.list"
          max-tag-count="responsive" />
        <n-select v-model:value="course_time.filter" multiple :options="course_time.list"
          max-tag-count="responsive" />
        <n-button block @click="Filter" :disabled="loading">筛选</n-button>
      </n-space>

    </n-card>
    <n-alert :show-icon="false" type="info">
      总学分：{{ stat.credit }}（{{ stat.num }}门）<br />
      个人学分绩 | GPA：{{ stat.score }} | {{ stat.gpa }}<br />
      估计平均绩 | GPA：{{ stat.avg_score }} | {{ stat.avg_gpa }}<br />
      <span style="color:#aaa">Tips:
        学分绩根据筛选出的课程加权计算，估计平均学分绩使用各科平均分计算得出，4分制GPA采用<a style="color:#888" target="_blank"
          href="https://jwc.bit.edu.cn/jwyx/cjgl/fe90fb3818184909bfc9228aada43970.htm">官方公式</a>计算。点击每行可查看详情。</span>
    </n-alert>

    <n-data-table :columns="columns" :data="data" size="small" striped :max-height="424" :scroll-x="715"
      :loading="loading" :row-props="RowProps" />
    <br />

    <n-modal v-model:show="modal" preset="card" style="width: 424px;" :title="modal_data['课程名称'] + ' 详情'">
      <div v-for="(value, key, index) in modal_data">{{ key + ': ' + value }}</div>
    </n-modal>
  </div>
</template>