<!--
 * @Author: flwfdd
 * @Date: 2022-02-20 23:45:13
 * @LastEditTime: 2022-02-22 22:17:05
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
        <v-card-title>
          {{ name }}
          <v-btn icon color="white" @click="GetList"
            ><v-icon>refresh</v-icon></v-btn
          ></v-card-title
        >
        <v-card-text class="white--text">
          个人学分绩：{{ score_sum / credit_sum }}<br />
          估计平均学分绩：{{ avg_score_sum / credit_sum }}<br />
          总学分：{{ credit_sum }}
        </v-card-text>
        <v-divider />
        <v-card-title>
          成寄单
          <v-spacer></v-spacer>
          <v-text-field
            v-model="table_search"
            append-icon="search"
            label="筛选"
            color="white--text"
          ></v-text-field>
        </v-card-title>
        <v-data-table
          :headers="table_headers"
          :items="score_list"
          :search="table_search"
          :items-per-page="233"
          :custom-sort="CustomSort"
        ></v-data-table>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "HomeView",
  data: () => ({
    name: "",
    msg: "2333",
    score_list: [],
    table_search: "",
    table_headers: [
      { text: "课程名称", value: "课程名称" },
      { text: "成绩", value: "本人成绩" },
      { text: "平均分", value: "平均分" },
      { text: "学分", value: "学分" },
      { text: "班级排名", value: "本人成绩在班级中占" },
      { text: "专业排名", value: "本人成绩在专业中占" },
      { text: "开课学期", value: "开课学期" },
    ],
    credit_sum: 0,
    score_sum: 0,
    avg_score_sum: 0,
    time_stamp: 0,
  }),
  created() {
    this.GetList();
  },
  methods: {
    GetList() {
      let time_stamp = ++this.time_stamp;
      this.$axios
        .get(
          this.$store.state.base_url +
            "/https/77726476706e69737468656265737421fae04c8f69326144300d8db9d6562d/jsxsd/kscj/cjcx_list"
        )
        .then((res) => {
          if (time_stamp != this.time_stamp) {
            return;
          }
          this.score_list = [];
          this.credit_sum = 0;
          this.score_sum = 0;
          this.avg_score_sum = 0;

          let parser = new DOMParser();
          let dom = parser.parseFromString(res.data, "text/html");
          this.name = dom.getElementById("Top1_divLoginName").innerHTML;
          let data_list = dom.getElementById("dataList").querySelectorAll("tr");
          let table = [];
          for (let tr of data_list) {
            let row = [];
            for (let i of tr.children) {
              row.push(i.innerHTML);
            }
            table.push(row);
          }
          for (let i = 1; i < table.length; i++) {
            let row = {};
            for (let j in table[i]) {
              row[table[0][j]] = table[i][j];
            }
            this.score_list.push(row);
          }
          // 解析成绩详情
          for (let sub of this.score_list) {
            if ("操作栏" in sub) {
              let url = /\/jsxsd\/kscj\/cjfx.+cjfs/.exec(sub["操作栏"]);
              if (url) {
                url = url[0];
              } else {
                continue;
              }
              url =
                this.$store.state.base_url +
                "/http/77726476706e69737468656265737421fae04c8f69326144300d8db9d6562d" +
                url.replaceAll("&amp;", "&");
              this.$axios
                .get(url)
                .then((res) => {
                  if (time_stamp != this.time_stamp) {
                    return;
                  }
                  let dom = parser.parseFromString(res.data, "text/html");
                  let data_list = dom.querySelectorAll("td");
                  for (let i of data_list) {
                    if (i.innerHTML.search("：") != -1) {
                      let kv = i.innerHTML.split("：");
                      this.$set(sub, kv[0], kv[1]);
                    }
                  }
                  if ("本人成绩" in sub) {
                    this.score_sum +=
                      Number(sub["本人成绩"]) * Number(sub["学分"]);
                    this.avg_score_sum +=
                      Number(sub["平均分"]) * Number(sub["学分"]);
                    this.credit_sum += Number(sub["学分"]);
                  }
                })
                .catch((err) => {
                  console.log(err);
                });
            }
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    CustomSort(items, sortBy, sortDesc) {
      if (sortBy.length) {
        let k = sortBy[0];
        items.sort((a, b) => {
          if (!isNaN(Number(a[k]))) {
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
  },
};
</script>