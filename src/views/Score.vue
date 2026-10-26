<!--
 * @Author: flwfdd
 * @Date: 2022-06-26 18:52:08
 * @LastEditTime: 2024-02-26 17:20:06
 * @Description: 
 * _(:з」∠)_
-->
<script setup lang="ts">
import router from "@/router";
import http from "@/utils/request";
import { hasSchoolCookie, isSchoolAuthRequired, schoolSession, withSchoolSession } from "@/utils/school";
import { clearSchoolResults, readSchoolCache, resultKey, writeSchoolCache } from "@/utils/school-cache";
import { FormatTime } from "@/utils/tools";
import store from "@/utils/store";
import { DataTableRowKey } from "naive-ui";
import { RowData } from "naive-ui/es/data-table/src/interface";
import { reactive, ref, onMounted, watch } from "vue";

const user = reactive({
  sid: store.grade_query.sid || schoolSession.sid || "",
  password: "",
});

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
  };
}

const columns = [
  {
    type: "selection",
    fixed: "left",
  },
  {
    title: "课程名称",
    key: "课程名称",
    fixed: "left",
    width: 99,
    sorter: "default",
    cellProps: (row: RowData) => {
      return {
        style: "cursor: pointer;",
        onClick: () => {
          modal_data.value = row;
          modal.value = true;
        },
      };
    },
  },
  {
    title: "成绩",
    key: "成绩",
    width: 66,
    sorter: CustomSorter("成绩"),
  },
  {
    title: "平均分",
    key: "平均分",
    width: 88,
    sorter: CustomSorter("平均分"),
  },
  {
    title: "学分",
    key: "学分",
    width: 66,
    sorter: CustomSorter("学分"),
  },
  {
    title: "班级排名",
    key: "本人成绩在班级中占",
    width: 99,
    sorter: CustomSorter("本人成绩在班级中占"),
  },
  {
    title: "专业排名",
    key: "本人成绩在专业中占",
    width: 99,
    sorter: CustomSorter("本人成绩在专业中占"),
  },
  {
    title: "开课学期",
    key: "开课学期",
    width: 99,
    sorter: "default",
  },
  {
    title: "课程性质",
    key: "课程性质",
    width: 99,
    sorter: "default",
  },
];

const ori_data = ref([] as any);
const data = ref([] as any);
const loading = ref(false);
const detail = ref(readSchoolCache<boolean>("score-detail")?.data === true);
const search = ref("");
const scoreCachedAt = ref(0);
const requestGeneration = ref(0);
const state = reactive({
  base_loaded: false,
  need_auth: false,
});
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
});

// 生成选择行的key
function rowKey(row: RowData) {
  return row["序号"];
}

// 选择框
const checkedRowKeys = ref<DataTableRowKey[]>([]);
watch(checkedRowKeys, () => {
  Compute();
});

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
    if (checkedRowKeys.value.indexOf(i["序号"]) != -1) {
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
  if (credit_sum === 0) {
    stat.credit = 0;
    stat.score = "";
    stat.gpa = "";
    stat.avg_score = "";
    stat.avg_gpa = "";
    return;
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
      if (x) {
        //已经添加过相同课程
        if (Score2Num(x["成绩"]) < score) {
          //替换
          checkedRowKeys.value.splice(
            checkedRowKeys.value.indexOf(x["序号"]),
            1
          );
          checkedRowKeys.value.push(i["序号"]);
          t[i["课程编号"]] = i;
        }
      } else {
        t[i["课程编号"]] = i;
        checkedRowKeys.value.push(i["序号"]);
      }
    }
  }

  store.grade_query.course_type_filter = course_type.filter;
  store.grade_query.course_time_filter = course_time.filter;

  Compute();
}

function ApplyScoreTable(table: string[][], _detail: boolean) {
  if (!Array.isArray(table) || table.length === 0 || !Array.isArray(table[0])) {
    throw new Error("成绩数据格式不正确");
  }
  const ori_head = table[0];
  ori_data.value = [];
  for (let i = 1; i < table.length; i++) {
    const row: Record<string, string> = {};
    for (const j in table[i]) {
      row[ori_head[j]] = table[i][j];
    }
    ori_data.value.push(row);
  }
  let s;
  const course_type_tmp: string[] = [];
  const course_time_tmp: string[] = [];
  course_type.list = [];
  course_time.list = [];
  for (const i of ori_data.value) {
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

  if (!course_type.filter || course_type.filter.length == 0)
    course_type.filter = course_type_tmp.concat();
  else
    course_type.filter = course_type.filter.filter(
      (s: string) => course_type_tmp.indexOf(s) != -1
    );

  if (!course_time.filter || course_time.filter.length == 0)
    course_time.filter = course_time_tmp.concat();
  else
    course_time.filter = course_time.filter.filter(
      (s: string) => course_time_tmp.indexOf(s) != -1
    );

  Filter();
  detail.value = _detail;
  writeSchoolCache("score-detail", _detail);
  state.base_loaded = true;
}

function RestoreScoreCache(): boolean {
  const sid = user.sid.trim();
  const cached = readSchoolCache<string[][]>(resultKey("score", sid, detail.value));
  if (!cached || !Array.isArray(cached.data) || cached.data.length === 0) {
    if (detail.value) {
      detail.value = false;
      writeSchoolCache("score-detail", false);
      return RestoreScoreCache();
    }
    return false;
  }
  ApplyScoreTable(cached.data, detail.value);
  scoreCachedAt.value = cached.cachedAt;
  store.grade_query.sid = sid;
  state.need_auth = false;
  return true;
}

function HandleSchoolError(error: any, fallback: string) {
  if (isSchoolAuthRequired(error)) state.need_auth = true;
  if (!error?.response && !error?.__bit101Notified) window.$message.error(error?.message || fallback);
}

async function GetList(username: string, password: string, _detail = false) {
  loading.value = true;
  const sid = username.trim();
  const generation = requestGeneration.value;
  try {
    const res = await withSchoolSession(sid, password, (cookie) => http.get("/score", {
      params: { detail: _detail },
      headers: { "webvpn-cookie": cookie },
    }));
    if (generation !== requestGeneration.value || user.sid.trim() !== sid) return;
    const table = res.data.data;
    ApplyScoreTable(table, _detail);
    store.grade_query.sid = sid;
    scoreCachedAt.value = Math.floor(Date.now() / 1000);
    writeSchoolCache(resultKey("score", sid, _detail), table);
    state.need_auth = false;
  } catch (error: any) {
    HandleSchoolError(error, "查询成绩失败");
  } finally {
    loading.value = false;
  }
}

function downloadCsv() {
  let csv =
    "课程名称,成绩,平均分,学分,本人成绩在班级中占,本人成绩在专业中占,开课学期,课程性质\n";
  for (let i of data.value) {
    csv += `${i["课程名称"]},${i["成绩"]},${i["平均分"]},${i["学分"]},${i["本人成绩在班级中占"]},${i["本人成绩在专业中占"]},${i["开课学期"]},${i["课程性质"]}\n`;
  }

  // 为了 Excel 的兼容性，添加 BOM
  const bom = new Uint8Array([0xef, 0xbb, 0xbf]);
  let blob = new Blob([bom, csv], { type: "text/csv;charset=utf-8" });
  let url = window.URL.createObjectURL(blob);
  let a = document.createElement("a");
  a.href = url;
  a.download = `Scores-BIT101-${new Date().toISOString()}.csv`;
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
  images: [] as string[],
  cachedAt: 0,
});

function ResetScoreView() {
  detail.value = false;
  writeSchoolCache("score-detail", false);
  search.value = "";
  state.base_loaded = false;
  state.need_auth = false;
  ori_data.value = [];
  data.value = [];
  checkedRowKeys.value = [];
  scoreCachedAt.value = 0;
  report.images = [];
  report.cachedAt = 0;
  report.modal = false;
  modal.value = false;
  modal_data.value = {};
  course_type.list = [];
  course_time.list = [];
  course_type.filter = [];
  course_time.filter = [];
  store.grade_query.course_type_filter = [];
  store.grade_query.course_time_filter = [];
  Object.assign(stat, { credit: 0, num: 0, score: "", gpa: "", avg_score: "", avg_gpa: "" });
}

function RestoreReportCache(): boolean {
  const cached = readSchoolCache<string[]>(resultKey("report", user.sid.trim()));
  if (!cached || !Array.isArray(cached.data) || cached.data.length === 0) return false;
  report.images = cached.data;
  report.cachedAt = cached.cachedAt;
  return true;
}

async function GetReport(username: string, password: string, refresh = false) {
  if (!refresh && RestoreReportCache()) {
    report.modal = true;
    return;
  }
  report.loading = true;
  const sid = username.trim();
  const generation = requestGeneration.value;
  try {
    const res = await withSchoolSession(sid, password, (cookie) => http.get("/score/report", {
      headers: { "webvpn-cookie": cookie },
    }));
    if (generation !== requestGeneration.value || user.sid.trim() !== sid) return;
    if (!Array.isArray(res.data.data) || res.data.data.length === 0) {
      throw new Error("可信成绩单为空");
    }
    report.images = res.data.data;
    report.cachedAt = Math.floor(Date.now() / 1000);
    writeSchoolCache(resultKey("report", sid), report.images);
    report.modal = true;
    state.need_auth = false;
  } catch (error: any) {
    HandleSchoolError(error, "获取可信成绩单失败");
    if (state.need_auth) report.modal = false;
  } finally {
    report.loading = false;
  }
}

function ClearScoreCache() {
  requestGeneration.value++;
  clearSchoolResults("score", user.sid.trim());
  clearSchoolResults("report", user.sid.trim());
  ResetScoreView();
  window.$message.success("已清除本地成绩缓存");
}

onMounted(() => {
  RestoreScoreCache();
  RestoreReportCache();
});

watch(() => user.sid, (sid, previous) => {
  if (sid === previous) return;
  requestGeneration.value++;
  ResetScoreView();
  RestoreScoreCache();
  RestoreReportCache();
});

watch(() => schoolSession.cookie, (value, previous) => {
  if (previous && !value) user.password = "";
});
</script>

<template>
  <n-space vertical>
    <n-card title="成寄查询">
      <n-space vertical v-if="!state.base_loaded || state.need_auth">
        <n-input
          :input-props="{ id: 'sid' }"
          v-model:value="user.sid"
          type="number"
          placeholder="学号"
          :disabled="loading || schoolSession.loading"
        />
        <n-input
          :input-props="{ id: 'password' }"
          v-model:value="user.password"
          type="password"
          show-password-on="click"
          placeholder="学校统一身份认证密码"
          :disabled="loading || schoolSession.loading"
        />
        <p v-if="hasSchoolCookie(user.sid)">已有学校会话，密码可留空。</p>
        <n-button
          id="submit"
          attr-type="submit"
          @click="GetList(user.sid, user.password, detail)"
          :disabled="!user.sid || (!user.password && !hasSchoolCookie(user.sid)) || loading || schoolSession.loading"
          block
          :loading="loading || schoolSession.loading"
        >
          查询
        </n-button>
        <n-button v-if="state.base_loaded" text @click="ClearScoreCache" :disabled="loading || report.loading || schoolSession.loading">清除本地缓存</n-button>
      </n-space>
      <n-space vertical v-else>
        <n-button
          @click="GetList(user.sid, user.password, detail)"
          :disabled="loading || schoolSession.loading"
          :loading="loading || schoolSession.loading"
          block
        >
          刷新成绩
        </n-button>
        <n-button
          v-show="!detail"
          @click="GetList(user.sid, user.password, true)"
          :disabled="loading || schoolSession.loading || detail"
          block
        >
          查询详细信息
        </n-button>
        <n-button
          @click="GetReport(user.sid, user.password)"
          :disabled="loading || schoolSession.loading || report.loading"
          :loading="report.loading"
          block
        >
          获取可信成绩单
        </n-button>
        <n-button @click="state.need_auth = true" :disabled="loading || schoolSession.loading || report.loading" block>
          重新认证
        </n-button>
        <n-button @click="ClearScoreCache" :disabled="loading || report.loading || schoolSession.loading" block>
          清除本地缓存
        </n-button>
        <p v-if="scoreCachedAt">上次更新：{{ FormatTime(scoreCachedAt) }}</p>
        <n-select
          v-model:value="course_type.filter"
          multiple
          :options="course_type.list"
          max-tag-count="responsive"
        />
        <n-select
          v-model:value="course_time.filter"
          multiple
          :options="course_time.list"
          max-tag-count="responsive"
        />
        <n-button block @click="Filter" :disabled="loading">筛选</n-button>
        <n-button
          block
          @click="downloadCsv"
          :disabled="loading || stat.num == 0"
        >
          导出为 CSV
        </n-button>
      </n-space>
    </n-card>
    <n-alert :show-icon="false" type="info">
      <p
        style="
          color: var(--text-color-3);
          font-size: 0.9em;
          line-height: 1.2em;
          margin-top: 0;
        "
      >
        Tips:
        学分绩根据筛选出的课程加权计算，估计平均绩使用各科平均分计算得出，4分制GPA采用
        <n-a
          href="https://jwb.bit.edu.cn/tzgg/0fd24ee94b774575ba1a9a4485f45b6c.htm"
          >官方公式</n-a
        >
        计算。可手动勾选纳入计算的课程，点击课程名称可查看详情。更多说明请见：
        <n-a href="/paper/20">BIT101常见问题解惑</n-a>
      </p>
      总学分：{{ stat.credit }}（{{ stat.num }}门）<br />
      个人学分绩 | GPA：{{ stat.score }} | {{ stat.gpa }}<br />
      <template v-if="detail"
        >估计平均绩 | GPA：{{ stat.avg_score }} | {{ stat.avg_gpa }}<br
      /></template>
    </n-alert>

    <n-data-table
      :columns="columns"
      :data="data"
      size="small"
      striped
      :scroll-x="777"
      :loading="loading"
      :pagination="{ pageSlot: 7 }"
      :row-key="rowKey"
      v-model:checked-row-keys="checkedRowKeys"
    />
    <br />

    <n-modal
      v-model:show="modal"
      preset="card"
      style="width: 424px"
      :title="modal_data['课程名称'] + ' 详情'"
    >
      <n-scrollbar style="max-height: 88vh">
        <n-button
          @click="
            (modal = false),
              router.push('/course/?search=' + modal_data['课程编号'])
          "
          >查找课程评价和资料</n-button
        >
        <div v-for="(value, key, index) in modal_data">
          {{ key + ": " + value }}
        </div>
      </n-scrollbar>
    </n-modal>

    <n-modal
      v-model:show="report.modal"
      preset="card"
      style="text-align: center; max-width: 666px"
    >
      <p v-if="report.cachedAt">上次更新：{{ FormatTime(report.cachedAt) }}</p>
      <n-button block :loading="report.loading" @click="GetReport(user.sid, user.password, true)">
        刷新可信成绩单
      </n-button>
      <n-scrollbar style="max-height: 88vh">
        <n-image
          v-for="(image, index) in report.images"
          :key="index"
          :src="image"
          :img-props="{ style: 'width:100%;' }"
        ></n-image>
      </n-scrollbar>
    </n-modal>
  </n-space>
</template>
