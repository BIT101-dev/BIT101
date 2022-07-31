<!--
 * @Author: flwfdd
 * @Date: 2022-07-10 23:03:43
 * @LastEditTime: 2022-07-31 17:55:22
 * @Description: 显示文章
 * _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import store from '@/utils/store';
import { onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import PaperRender from '@/components/PaperRender.vue';
import { FormatTime, Clip } from '@/utils/tools';
import { EditOutlined, ThumbUpOutlined, ThumbUpFilled, ShareOutlined } from '@vicons/material';
import Comment from '@/components/Comment.vue';

//文章数据
const paper = reactive({
  id: "",
  title: "俺是标题！",
  intro: "",
  data: {},
  create_time: "",
  update_time: "",
  user: {
    id: 0,
    nickname: "",
    avatar: "",
  },
  like_num: 0,
  like: false,
  like_loading: false,
  comment_num:0,
  share:true,
  own:false,
})

//加载文章
function LoadPaper() {
  http.get("/paper/?id=" + paper.id)
    .then(res => {
      paper.title = res.data.title;
      paper.intro = res.data.intro;
      paper.data = JSON.parse(res.data.data);
      paper.create_time = FormatTime(res.data.create_time);
      paper.update_time = FormatTime(res.data.update_time);
      paper.user.id = res.data.anonymous ? '-1' : res.data.user;
      paper.like_num = res.data.like_num;
      paper.comment_num=res.data.comment_num;
      paper.like = res.data.like;
      paper.user = res.data.user;
      paper.share=res.data.share;
      paper.own=res.data.own;
    })
}

function Like() {
  paper.like_loading = true;
  http.post("/reaction/like/", { 'obj': 'paper' + paper.id })
    .then(res => {
      paper.like = res.data.like;
      paper.like_num = res.data.like_num;
      paper.like_loading = false;
    }).catch(() => { paper.like_loading = false; })
}

function ClipUrl() {
  Clip(window.location.href, "文章链接已复制OvO");
}

const router = useRouter();
const route = useRoute();
paper.id = route.params.id as string;
onMounted(() => {
  LoadPaper();
})
</script>

<template>
  <div class="container">
    <div style="text-align:center;">
      <h2 style="color:#00BCD4">{{ paper.title }}</h2>
    </div>
    <n-divider></n-divider>
    <div style="display: flex;align-items: center;color:#3E5C6B;">
      <a :href="'/#/user/' + paper.user.id" target="_blank">
        <n-avatar :src="paper.user.avatar + store.img_suffix" />
      </a>
      <span style="margin-left: 4px;margin-top:-6px;">
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
        {{ paper.like_num }}人赞同
      </n-button>
      <n-button @click="ClipUrl" icon-placement="right" ghost>
        <template #icon>
          <n-icon>
            <ShareOutlined />
          </n-icon>
        </template>
        分享
      </n-button>
    </n-space>

    <n-divider style="color:#809BA8;font-size:14px;">首次编辑于{{ paper.create_time }}</n-divider>
    <PaperRender :paper="paper" />
    <n-divider style="color:#809BA8;font-size:14px;">
      <n-button v-if="(paper.share || paper.own)" @click="router.push('/paper/edit/' + paper.id)" icon-placement="right" text>
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
      <n-button @click="ClipUrl" icon-placement="right" ghost>
        <template #icon>
          <n-icon>
            <ShareOutlined />
          </n-icon>
        </template>
        分享
      </n-button>
      <n-button @click="Like" icon-placement="right" color="#fb7299" :ghost="!paper.like" :loading="paper.like_loading"
        :disabled="paper.like_loading">
        <template #icon>
          <n-icon>
            <ThumbUpFilled v-if="paper.like" />
            <ThumbUpOutlined v-else />
          </n-icon>
        </template>
        {{ paper.like_num }}人赞同
      </n-button>
    </n-space>
    <n-divider style="color:#809BA8;font-size:14px;">现有{{paper.comment_num}}条评论</n-divider>
    <Comment :obj='"paper" + paper.id'></Comment>
  </div>
</template>