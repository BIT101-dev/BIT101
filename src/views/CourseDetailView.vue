<!--
 * @Author: flwfdd
 * @Date: 2022-03-18 16:00:17
 * @LastEditTime: 2022-03-19 23:27:53
 * @Description: 
 * _(:з」∠)_
-->
<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="11">
        <v-card class="my-4">
          <v-card-title>{{ data.name }}</v-card-title>
          <v-card-text>
            授课教师：{{ data.teachers_name }}
            <v-btn
              icon
              x-small
              color="cyan"
              @click="Search('', data.teachers_name)"
              ><v-icon>search</v-icon></v-btn
            ><br />
            课程编号：{{ data.number }}
            <v-btn icon x-small color="cyan" @click="Search(data.number, '')"
              ><v-icon>search</v-icon></v-btn
            >
            <v-rating
              half-increments
              :value="data.rating_sum / data.rater_sum / 2"
              color="pink lighten-3"
              background-color="cyan"
              readonly
              large
            ></v-rating>
            {{ data.rating_sum / data.rater_sum / 2 }} 分（共有
            {{ data.rater_sum }} 人参与评分
            <br />
            <v-btn outlined color="cyan" @click="dialog = true" class="mt-2"
              >我要指点江山</v-btn
            >
          </v-card-text>
        </v-card>

        <v-card class="my-4" v-for="i in rate_list" :key="i.id">
          <v-card-text>
            <v-avatar size="42" v-if="i.anonymous == false"
              ><SelfImg :src="i.user.avatar"></SelfImg
            ></v-avatar>
            {{ i.anonymous ? "匿名者" : i.user.nickname }}
            {{ FormatDate(i.time) }}
            <v-rating
              :value="i.rating / 2"
              readonly
              half-increments
              color="pink lighten-3"
              background-color="cyan"
            ></v-rating>
            <p style="white-space: pre-line" class="mx-2">{{ i.comment }}</p>
            <v-btn icon @click="Like(i)">
              <v-icon v-if="!i.like">mdi-thumb-up-outline</v-icon>
              <v-icon v-else color="pink lighten-3">mdi-thumb-up</v-icon>
            </v-btn>
            {{ i.like_sum }}人赞同
          </v-card-text>
        </v-card>

        <v-btn
          block
          class="my-4"
          color="cyan lighten-2"
          :disabled="end != 0"
          :loading="end == -1"
          @click="GetRate"
        >
          {{ end == 1 ? "木有更多了" : "加载更多" }}
        </v-btn>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog">
      <v-card>
        <v-card-title
          >评教
          <v-spacer />
          <v-switch label="匿名" color="cyan" v-model="anonymous"></v-switch>
        </v-card-title>
        <v-card-text>
          重复评教将会覆盖
          <v-rating
            half-increments
            v-model="rating"
            color="pink lighten-3"
            background-color="cyan"
            large
          ></v-rating>

          <v-textarea
            label="谈谈感想吧(｡･∀･)ﾉﾞ"
            v-model="comment"
            outlined
            color="cyan"
          ></v-textarea>
          <v-btn outlined block color="cyan" @click="Submit">提交</v-btn>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import SelfImg from "@/components/SelfImg.vue";
import { FormatDate } from "@/components/GlobalMethod";

export default {
  components: {
    SelfImg,
  },
  data: () => ({
    data: {},
    dialog: false,
    rating: 5,
    comment: "孩子很喜欢，下次还来。",
    anonymous: false,
    page: 0,
    rate_list: [],
    end: 0,
  }),
  methods: {
    Get() {
      this.$axios
        .get(this.$store.state.api_url + "/course/detail/", {
          params: {
            id: this.$route.query.id,
          },
        })
        .then((res) => {
          this.data = res.data;
        })
        .catch((err) => {
          console.log(err);
          this.$store.commit("msg", "出错了Orz");
        });
      this.page = 0;
      this.rate_list = [];
      this.GetRate();
    },
    GetRate() {
      this.end = -1;
      this.$axios
        .get(this.$store.state.api_url + "/course/rate_list/", {
          params: {
            id: this.$route.query.id,
            page: this.page++,
          },
        })
        .then((res) => {
          this.rate_list = this.rate_list.concat(res.data);
          this.end = !res.data.length;
        })
        .catch((err) => {
          console.log(err);
          this.$store.commit("msg", "出错了Orz");
        });
    },
    Submit() {
      console.log(this.rating);
      this.$axios
        .get(this.$store.state.api_url + "/course/rate/", {
          params: {
            id: this.data.id,
            rating: this.rating * 2,
            comment: this.comment,
            anonymous: this.anonymous ? 1 : 0,
          },
        })
        .then(() => {
          this.dialog = false;
          this.Get();
          this.$store.commit("msg", "提交成功OvO");
        })
        .catch(() => {
          this.$store.commit("msg", "提交失败Orz");
        });
    },
    FormatDate(t) {
      return FormatDate(t);
    },
    Like(i) {
      if (i.like) i.like_sum--;
      else i.like_sum++;
      i.like = !i.like;
      this.$axios
        .get(this.$store.state.api_url + "/course/rate_like/", {
          params: {
            id: i.id,
            like: i.like ? 1 : 0,
          },
        })
        .then(() => {
          this.$store.commit("msg", "点赞成功OvO");
        })
        .catch(() => {
          this.$store.commit("msg", "点赞失败Orz");
        });
    },
    Search(course, teacher) {
      this.$router.push("/course?course=" + course + "&teacher=" + teacher);
    },
  },
  created() {
    this.Get();
  },
};
</script>

<style>
</style>