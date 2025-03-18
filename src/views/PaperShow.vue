<!--
 * @Author: flwfdd
 * @Date: 2022-07-10 23:03:43
 * @LastEditTime: 2025-03-19 01:40:23
 * @Description: 显示文章
 * _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import { onMounted, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import PaperRender from '@/components/PaperRender.vue';
import { FormatTime, setTitle, Share } from '@/utils/tools';
import EditOutlined from '@vicons/material/EditOutlined'
import ThumbUpOutlined from '@vicons/material/ThumbUpOutlined'
import ThumbUpFilled from '@vicons/material/ThumbUpFilled'
import BookmarkFilled from '@vicons/material/BookmarkFilled'
import BookmarkOutlined from '@vicons/material/BookmarkOutlined'
import ShareOutlined from '@vicons/material/ShareOutlined'
import Comment from '@/components/Comment.vue';
import Avatar from '@/components/Avatar.vue';
import { SubscriptionLevel, User } from '@/utils/types';
import Subscription from '@/components/Subscription.vue';

//文章数据
const paper = reactive({
  id: "",
  title: "俺是标题！",
  intro: "",
  data: {},
  create_time: "",
  update_time: "",
  user: {} as User,
  like_num: 0,
  like: false,
  like_loading: false,
  comment_num: 0,
  public_edit: true,
  own: false,
  subscription: SubscriptionLevel.None,
  subscription_loading: false,
})

//加载文章
function LoadPaper() {
  return http.get("/papers/" + paper.id)
    .then(res => {
      paper.title = res.data.title;
      paper.intro = res.data.intro;
      paper.data = JSON.parse(res.data.content);
      paper.create_time = FormatTime(res.data.create_time);
      paper.update_time = FormatTime(res.data.update_time);
      paper.like_num = res.data.like_num;
      paper.comment_num = res.data.comment_num;
      paper.like = res.data.like;
      paper.user = res.data.update_user;
      paper.public_edit = res.data.public_edit;
      paper.own = res.data.own;
      paper.subscription = res.data.subscription;
    })
}

function Like() {
  paper.like_loading = true;
  http.post("/reaction/like", { 'obj': 'paper' + paper.id })
    .then(res => {
      paper.like = res.data.like;
      paper.like_num = res.data.like_num;
      paper.like_loading = false;
    }).catch(() => { paper.like_loading = false; })
}

function SharePaper() {
  let title = 'BIT101文章｜' + paper.title;
  Share(title, title, window.location.href)
}

const router = useRouter();
const route = useRoute();
paper.id = route.params.id as string;
onMounted(async () => {
  await LoadPaper()
  setTitle(paper.title, '文章')
})
</script>

<template>
  <div class="container" v-if="paper.user.id">
    <div style="text-align:center;">
      <n-h2>{{ paper.title }}</n-h2>
    </div>
    <n-divider></n-divider>
    <div style="display: flex;align-items: center;">
      <router-link :to="'/user/' + paper.user.id">
        <Avatar :user="paper.user" :size="36" />
      </router-link>
      <span style="margin-left: 4px;">
        <div style="font-size: 16px;">{{ paper.user.nickname }}</div>
        <div style="margin-top: -4px;font-size:14px;">最后编辑于{{ paper.update_time }}</div>
      </span>

    </div>

    <n-space style="margin-top:4px">
      <n-button @click="Like" icon-placement="right" color="#fb7299" :ghost="!paper.like" :loading="paper.like_loading"
        :disabled="paper.like_loading">
        <template #icon>
          <n-icon>
            <ThumbUpFilled v-if="paper.like" />
            <ThumbUpOutlined v-else />
          </n-icon>
        </template>
        {{ paper.like_num }}赞同
      </n-button>

      <n-button @click="SharePaper" icon-placement="right" ghost>
        <template #icon>
          <n-icon>
            <ShareOutlined />
          </n-icon>
        </template>
        分享
      </n-button>

    </n-space>

    <n-divider style="color:var(--text-color-3);font-size:14px;">首次编辑于{{ paper.create_time }}</n-divider>
    <PaperRender :paper="paper" />
    <n-divider style="color:var(--text-color-3);font-size:14px;">
      <n-button v-if="(paper.public_edit || paper.own)" @click="router.push('/paper/edit/' + paper.id)"
        icon-placement="right" text>
        <template #icon>
          <n-icon>
            <EditOutlined />
          </n-icon>
        </template>
        编辑此篇Paper
      </n-button>
      <template v-else>不允许编辑</template>
    </n-divider>
    <n-space style="margin-top:4px" justify="end">
      <n-button @click="SharePaper" icon-placement="right" ghost>
        <template #icon>
          <n-icon>
            <ShareOutlined />
          </n-icon>
        </template>
        分享
      </n-button>

      <Subscription :obj="'paper' + paper.id" :level="paper.subscription" />

      <n-button @click="Like" icon-placement="right" color="#fb7299" :ghost="!paper.like" :loading="paper.like_loading"
        :disabled="paper.like_loading">
        <template #icon>
          <n-icon>
            <ThumbUpFilled v-if="paper.like" />
            <ThumbUpOutlined v-else />
          </n-icon>
        </template>
        {{ paper.like_num }}赞同
      </n-button>

    </n-space>
    <n-divider style="color:var(--text-color-3);font-size:14px;">现有{{ paper.comment_num }}条评论</n-divider>
    <Comment :obj='"paper" + paper.id'></Comment>
  </div>
</template>