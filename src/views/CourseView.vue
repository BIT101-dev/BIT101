<!--
 * @Author: flwfdd
 * @Date: 2022-03-19 13:57:34
 * @LastEditTime: 2022-03-19 23:30:17
 * @Description: 
 * _(:з」∠)_
-->
<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="11">
        <v-card>
          <v-card-title>课程检索</v-card-title>
          <v-card-subtitle>分享学习经验、恣意指点江山……</v-card-subtitle>
          <v-card-text>
            <v-row>
              <v-col cols="6" class="pr-1">
                <v-text-field
                  v-model="course_search"
                  label="课程"
                  hint="课程名或编号"
                  outlined
                  color="cyan"
                ></v-text-field>
              </v-col>
              <v-col cols="6" class="pl-1">
                <v-text-field
                  v-model="teacher_search"
                  label="教师"
                  hint="教师姓名"
                  outlined
                  color="cyan"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-btn
              block
              outlined
              color="cyan"
              @click="StartSearch"
              :loading="end == -1"
              >GET IT!</v-btn
            >
          </v-card-text>
        </v-card>

        <v-card v-for="i in data" :key="i.id" class="my-4" @click="Jump(i.id)">
          <v-card-title>{{ i.name }}</v-card-title>
          <v-card-text>
            编号：{{ i.number }}<br />
            教师：{{ i.teachers_name }}
            <v-rating
              half-increments
              :value="i.rating_sum / i.rater_sum / 2"
              color="pink lighten-3"
              background-color="cyan"
              readonly
            ></v-rating>
            {{ i.rating_sum / i.rater_sum / 2 }} 分（共有
            {{ i.rater_sum }} 人参与评分
          </v-card-text>
        </v-card>

        <v-btn
          block
          class="my-4"
          color="cyan lighten-2"
          :disabled="end != 0"
          :loading="end == -1"
          @click="Search"
        >
          {{ end == 1 ? "木有更多了" : "加载更多" }}
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    data: [],
    course_search: "",
    teacher_search: "",
    page: 0,
    end: 0,
  }),
  methods: {
    Search() {
      this.end = -1;
      this.$axios
        .get(this.$store.state.api_url + "/course/search/", {
          params: {
            course_search: this.course_search,
            teacher_search: this.teacher_search,
            page: this.page++,
          },
        })
        .then((res) => {
          this.data = this.data.concat(res.data);
          this.end = !res.data.length;
        })
        .catch((err) => {
          console.log(err);
          this.$store.commit("msg", "出错了Orz");
        });
    },
    StartSearch() {
      this.end = 0;
      this.data = [];
      this.page = 0;
      this.Search();
    },
    Jump(id) {
      this.$router.push("/course/detail?id=" + id);
    },
  },
  created() {
    if (this.$route.query.course || this.$route.query.teacher) {
      this.course_search = this.$route.query.course;
      this.teacher_search = this.$route.query.teacher;
      this.StartSearch();
    }
  },
};
</script>