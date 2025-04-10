<!--
 * @Author: flwfdd
 * @Date: 2022-06-26 18:52:08
 * @LastEditTime: 2024-02-26 17:20:06
 * @Description: 
 * _(:з」∠)_
-->
<script setup lang="ts">
import router from '@/router';
import http from '@/utils/request';
import { WebvpnVerify, webvpn } from '@/utils/tools';
import store from '@/utils/store';
import { DataTableRowKey } from 'naive-ui';
import { RowData } from 'naive-ui/es/data-table/src/interface';
import { reactive, ref, onMounted, watch } from 'vue';

const user = reactive({
  sid: store.grade_query.sid,
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
    type: 'selection',
    fixed: 'left',
  },
  {
    title: '课程名称',
    key: '课程名称',
    fixed: 'left',
    width: 99,
    sorter: 'default',
    cellProps: (row: RowData) => {
      return {
        style: 'cursor: pointer;',
        onClick: () => {
          modal_data.value = row;
          modal.value = true;
        }
      }
    }
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
  list: [] as any,
  filter: store.grade_query.course_type_filter,
});
const course_time = reactive({
  list: [] as any,
  filter: store.grade_query.course_time_filter,
});
const stat = reactive({
  credit: 0,
  num: 0,
  score: "",
  gpa: "",
  avg_score: "",
  avg_gpa: "",
})

// 生成选择行的key
function rowKey(row: RowData) {
  return row['序号']
}

// 选择框
const checkedRowKeys = ref<DataTableRowKey[]>([])
watch(checkedRowKeys, () => {
  Compute();
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

// 计算成绩
function Compute() {
  let credit_sum = 0;
  let score_sum = 0;
  let gpa_sum = 0;
  let avg_score_sum = 0;
  let avg_gpa_sum = 0;
  stat.num = 0;
  for (let i of ori_data.value) {
    if (checkedRowKeys.value.indexOf(i['序号']) != -1) {
      let credit = Number(i["学分"]);
      stat.num++;
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

// 筛选
function Filter() {
  data.value = [];
  checkedRowKeys.value = [];
  let t = {};
  for (let i of ori_data.value) {
    if (
      i["课程名称"].search(search.value) != -1 &&
      course_type.filter.indexOf(i["课程性质"]) != -1 &&
      course_time.filter.indexOf(i["开课学期"]) != -1
    ) {
      data.value.push(i);
      let score = Score2Num(i["成绩"]);
      if (score == 0) continue;
      let x = t[i["课程编号"]];
      if (x) { //已经添加过相同课程
        if (Score2Num(x["成绩"]) < score) { //替换
          checkedRowKeys.value.splice(checkedRowKeys.value.indexOf(x["序号"]), 1);
          checkedRowKeys.value.push(i["序号"]);
          t[i["课程编号"]] = i;
        }
      }
      else {
        t[i["课程编号"]] = i;
        checkedRowKeys.value.push(i["序号"]);
      }
    }
  }

  store.grade_query.course_type_filter = course_type.filter;
  store.grade_query.course_time_filter = course_time.filter;
  
  Compute();
}


function GetList() {
  if (!webvpn.cookie) return;
  loading.value = true;
  http
    .get("/score", {
      params: {
        detail: detail.value ? true : '',
      },
      headers: {
        "webvpn-cookie": webvpn.cookie,
      },
    })
    .then((res) => {
      store.grade_query.sid = user.sid;
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
      let course_type_tmp: string[] = [];
      let course_time_tmp: string[] = [];
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

      // 保留之前的筛选
      if(!course_type.filter || course_type.filter.length == 0)
        course_type.filter = course_type_tmp.concat();
      else
        course_type.filter = course_type.filter.filter((s: string) => course_type_tmp.indexOf(s) != -1);

      if(!course_time.filter || course_time.filter.length == 0)
        course_time.filter = course_time_tmp.concat();
      else
        course_time.filter = course_time.filter.filter((s: string) => course_time_tmp.indexOf(s) != -1);
      
      Filter();
    })
}

function downloadCsv() {
  let csv = "课程名称,成绩,平均分,学分,本人成绩在班级中占,本人成绩在专业中占,开课学期,课程性质\n";
  for (let i of data.value) {
    csv += `${i["课程名称"]},${i["成绩"]},${i["平均分"]},${i["学分"]},${i["本人成绩在班级中占"]},${i["本人成绩在专业中占"]},${i["开课学期"]},${i["课程性质"]}\n`;
  }
  
  // 为了 Excel 的兼容性，添加 BOM
  const bom = new Uint8Array([0xEF, 0xBB, 0xBF]);
  let blob = new Blob([bom, csv], { type: 'text/csv;charset=utf-8' });
  let url = window.URL.createObjectURL(blob);
  let a = document.createElement('a');
  a.href = url;
  a.download = `Scores-BIT101-${(new Date()).toISOString()}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
}

// 课程详情
const modal = ref(false);
const modal_data = ref({});

const report = reactive({
  loading: false,
  modal: false,
  list: [],
})
function GetReport() {
  report.loading = true;
  http.get('/score/report', {
    headers: {
      "webvpn-cookie": webvpn.cookie,
    },
  })
    .then((res) => {
      report.list = res.data.data;
      report.loading = false;
      report.modal = true;
    }).catch(() => {
      report.loading = false;
    })
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
        <n-input :input-props="{id:'sid'}" v-model:value="user.sid" type="number" placeholder="学号" />
        <n-input :input-props="{id:'password'}" v-model:value="user.password" type="password" show-password-on="click" placeholder="学校统一身份认证密码" />
        <n-button id="submit" attr-type="submit" @click="WebvpnVerify(user.sid, user.password)" :disabled="!user.sid || !user.password || webvpn.loading"
          block :loading="webvpn.loading">
          查询
        </n-button>
      </n-space>
      <n-space vertical v-else>
        <n-button v-show="!detail" @click="detail = true, GetList()" :disabled="loading || detail" block>
          查询详细信息
        </n-button>
        <n-button @click="GetReport()" :disabled="loading || report.loading" :loading="report.loading" block>
          获取可信成绩单
        </n-button>
        <n-select v-model:value="course_type.filter" multiple :options="course_type.list" max-tag-count="responsive" />
        <n-select v-model:value="course_time.filter" multiple :options="course_time.list" max-tag-count="responsive" />
        <n-button block @click="Filter" :disabled="loading">筛选</n-button>
        <n-button block @click="downloadCsv" :disabled="loading || stat.num == 0">
          导出为 CSV
        </n-button>
      </n-space>

    </n-card>
    <n-alert :show-icon="false" type="info">
      <p style="color:var(--text-color-3);font-size: 0.9em;line-height: 1.2em;margin-top: 0;">Tips:
        学分绩根据筛选出的课程加权计算，估计平均绩使用各科平均分计算得出，4分制GPA采用
        <n-a href="https://jwb.bit.edu.cn/tzgg/0fd24ee94b774575ba1a9a4485f45b6c.htm">官方公式</n-a>
        计算。可手动勾选纳入计算的课程，点击课程名称可查看详情。更多说明请见：
        <n-a href="/paper/20">BIT101常见问题解惑</n-a>
      </p>
      总学分：{{ stat.credit }}（{{ stat.num }}门）<br />
      个人学分绩 | GPA：{{ stat.score }} | {{ stat.gpa }}<br />
      <template v-if="detail">估计平均绩 | GPA：{{ stat.avg_score }} | {{ stat.avg_gpa }}<br /></template>
    </n-alert>

    <n-data-table :columns="columns" :data="data" size="small" striped :scroll-x="777" :loading="loading"
      :pagination="{ pageSlot: 7 }" :row-key="rowKey" v-model:checked-row-keys="checkedRowKeys" />
    <br />

    <n-modal v-model:show="modal" preset="card" style="width: 424px;" :title="modal_data['课程名称'] + ' 详情'">
      <n-scrollbar style="max-height:88vh;">
        <n-button @click="modal = false, router.push('/course/?search=' + modal_data['课程编号'])">查找课程评价和资料</n-button>
        <div v-for="(value, key, index) in modal_data">{{ key + ': ' + value }}</div>
      </n-scrollbar>
    </n-modal>

    <n-modal v-model:show="report.modal" preset="card" style="text-align:center;max-width: 666px;">
      <n-scrollbar style="max-height:88vh;">
        <n-image v-for="i in report.list" :src="i" :img-props="{ 'style': 'width:100%;' }"></n-image>
      </n-scrollbar>
    </n-modal>
  </div>
</template>
