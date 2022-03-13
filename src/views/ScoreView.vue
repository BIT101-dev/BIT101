<!--
 * @Author: flwfdd
 * @Date: 2022-02-20 23:45:13
 * @LastEditTime: 2022-03-13 11:48:31
 * @Description: 
 * _(:з」∠)_
-->

<template>
  <v-container>
    <v-row justify="center" class="ma-12">
      <h1 class="cyan--text">成绩查询</h1>
    </v-row>

    <v-row justify="center">
      <v-card color="cyan white--text">
        <v-card-text class="white--text">
          个人学分绩：{{ (score_sum / credit_sum).toFixed(4) }} |
          {{ (gpa_sum / credit_sum).toFixed(4) }}<br />
          估计平均绩：{{ (avg_score_sum / credit_sum).toFixed(4) }} |
          {{ (avg_gpa_sum / credit_sum).toFixed(4) }}<br />
          总学分：{{ credit_sum }}
        </v-card-text>
        <v-card-text class="white--text">
          Tips:
          学分绩根据筛选出的课程加权计算，估计平均学分绩使用各科平均分计算得出，4分制GPA采用<a
            class="white--text"
            target="_blank"
            href="https://jwc.bit.edu.cn/jwyx/cjgl/fe90fb3818184909bfc9228aada43970.htm"
            >官方公式</a
          >计算，点击表头可进行排序。
        </v-card-text>
        <v-divider />
        <v-card-title>
          <v-container fuild>
            <v-row
              >成寄单
              <v-switch
                v-model="detail"
                color="white"
                class="my-0 mx-2"
                :disabled="status < 0 || detail"
              >
                <template v-slot:label
                  ><span class="white--text">获取详情（加载较慢</span></template
                >
              </v-switch>
            </v-row>

            <v-row>
              <v-col cols="4" class="py-0 px-1">
                <v-select
                  v-model="course_type"
                  :items="course_type_list"
                  :menu-props="{ maxHeight: '424' }"
                  label="课程类型"
                  multiple
                  item-color="cyan"
                  color="white"
                >
                  <template v-slot:selection="{ index }">
                    <v-chip v-if="index === 0" small color="cyan lighten-4">
                      <span>+{{ course_type.length }}</span>
                    </v-chip>
                  </template>
                </v-select>
              </v-col>
              <v-col cols="4" class="py-0 px-1">
                <v-select
                  v-model="course_time"
                  :items="course_time_list"
                  :menu-props="{ maxHeight: '424' }"
                  label="开课学期"
                  multiple
                  item-color="cyan"
                  color="white"
                >
                  <template v-slot:selection="{ index }">
                    <v-chip v-if="index === 0" small color="cyan lighten-4">
                      <span>+{{ course_time.length }}</span>
                    </v-chip>
                  </template>
                </v-select>
              </v-col>
              <v-col cols="4" class="py-0 px-1">
                <v-text-field
                  v-model="search"
                  label="搜索"
                  color="white"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-btn block color="cyan lighten-4" @click="Filter">
                筛选<v-icon>search</v-icon>
              </v-btn>
            </v-row>
          </v-container>
        </v-card-title>
        <v-data-table
          :headers="table_headers"
          :items="table_items"
          :items-per-page="233"
          :custom-sort="CustomSort"
          :loading="status < 0"
        ></v-data-table>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import { Login } from "@/components/GlobalMethod";

export default {
  name: "HomeView",
  data: () => ({
    name: "",
    msg: "2333",
    score_list: [],
    table_headers: [
      { text: "课程名称", value: "课程名称" },
      { text: "成绩", value: "成绩" },
      { text: "平均分", value: "平均分" },
      { text: "学分", value: "学分" },
      { text: "班级排名", value: "本人成绩在班级中占" },
      { text: "专业排名", value: "本人成绩在专业中占" },
      { text: "开课学期", value: "开课学期" },
      { text: "课程性质", value: "课程性质" },
    ],
    table_items: [],
    credit_sum: 0,
    score_sum: 0,
    gpa_sum: 0,
    avg_score_sum: 0,
    avg_gpa_sum: 0,
    status: 0,
    search: "",
    course_type_list: [],
    course_type: [],
    course_time_list: [],
    course_time: [],
    detail: false,
  }),
  created() {
    this.GetList();
  },
  methods: {
    GetList() {
      if (this.status >= 0) this.status = -1;
      this.score_list = [];
      let url =
        this.$store.state.api_url +
        "/get_score" +
        (this.detail ? "_detail/" : "/");
      this.$axios
        .get(url, {
          params: {
            cookie: this.$store.state.webvpn_cookie,
          },
        })
        .then((res) => {
          this.status = 1;
          let ori_table = res.data;
          let ori_head = ori_table[0];
          this.score_list = [];
          for (let i = 1; i < ori_table.length; i++) {
            let row = {};
            for (let j in ori_table[i]) {
              row[ori_head[j]] = ori_table[i][j];
            }
            this.score_list.push(row);
          }
          let s;
          for (let i of this.score_list) {
            s = i["课程性质"];
            if (this.course_type_list.indexOf(s) == -1)
              this.course_type_list.push(s);
            s = i["开课学期"];
            if (this.course_time_list.indexOf(s) == -1)
              this.course_time_list.push(s);
          }
          this.course_type = this.course_type_list.concat();
          this.course_time = this.course_time_list.concat();
          this.Filter();
        })
        .catch((err) => {
          console.log(err);
          if (err.request.status == 424 && this.status != -2) {
            this.status = -2;
            Login(
              this.$store.state.webvpn_username,
              this.$store.state.webvpn_password
            ).then(() => {
              this.GetList();
            });
          }
        });
    },
    CustomSort(items, sortBy, sortDesc) {
      if (sortBy.length) {
        let k = sortBy[0];
        items.sort((a, b) => {
          if(!a[k] || !b[k])return 1;
          if (!isNaN(a[k])) {
            return a[k] - b[k];
          } else if (a[k].search("%") != -1) {
            return parseInt(a[k]) - parseInt(b[k]);
          } else {
            return a[k] < b[k] ? -1 : 1;
          }
        });
        if (sortDesc[0]) {
          items.reverse();
        }
      }

      return items;
    },
    Filter() {
      this.credit_sum = 0;
      this.score_sum = 0;
      this.gpa_sum = 0;
      this.avg_score_sum = 0;
      this.avg_gpa_sum = 0;
      this.table_items = [];
      for (let i of this.score_list) {
        if (
          i["课程名称"].search(this.search) != -1 &&
          this.course_type.indexOf(i["课程性质"]) != -1 &&
          this.course_time.indexOf(i["开课学期"]) != -1
        ) {
          let credit = Number(i["学分"]);
          if (isNaN(credit) || credit == 0) continue;
          let score = this.Score2Num(i["成绩"]);
          let avg_score = this.Score2Num(i["平均分"]);
          let gpa = this.Score2GPA(i["成绩"]);
          let avg_gpa = this.Score2GPA(i["平均分"]);
          this.credit_sum += credit;
          this.score_sum += score * credit;
          this.gpa_sum += gpa * credit;
          this.avg_score_sum += avg_score * credit;
          this.avg_gpa_sum += avg_gpa * credit;
          this.table_items.push(i);
        }
      }
      return true;
    },
    Score2Num(s) {
      let ind = ["优秀", "良好", "中等", "及格", "不及格"].indexOf(s);
      if (ind != -1) return [95, 85, 75, 65, 0][ind];
      return Number(s);
    },
    Score2GPA(s) {
      let ind = ["优秀", "良好", "中等", "及格", "不及格"].indexOf(s);
      if (ind != -1) return [4.0, 3.6, 2.8, 1.7, 0][ind];
      let x = Number(s);
      if (x < 60) return 0;
      return 4 - (3 * (100 - x) * (100 - x)) / 1600;
    },
  },
  watch: {
    detail() {
      this.GetList();
    },
  },
};
</script>