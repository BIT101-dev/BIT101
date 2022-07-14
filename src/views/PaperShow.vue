<!--
 * @Author: flwfdd
 * @Date: 2022-07-10 23:03:43
 * @LastEditTime: 2022-07-14 21:34:52
 * @Description: 显示文章
 * _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import store from '@/utils/store';
import { onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import PaperRender from '@/components/PaperRender.vue';
import { FormatTime,Clip } from '@/utils/tools';
import { EditOutlined, ThumbUpOutlined, ThumbUpFilled, ShareOutlined } from '@vicons/material';

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
  like_num:0,
  like: false,
})

function GetUserInfo() {
  http.get("/user/info/?id=" + paper.user.id)
    .then(res => {
      paper.user.id = res.data.id;
      paper.user.nickname = res.data.nickname;
      paper.user.avatar = res.data.avatar;
    })
}

//加载文章
function LoadPaper() {
  paper.id = route.params.id as string;
  http.get("/paper/?id=" + paper.id)
    .then(res => {
      paper.title = res.data.title;
      paper.intro = res.data.intro;
      paper.data = JSON.parse(res.data.data);
      paper.create_time = FormatTime(res.data.create_time);
      paper.update_time = FormatTime(res.data.update_time);
      paper.user.id = res.data.user;
      paper.like_num=res.data.like_num;
      paper.like=res.data.like;
      GetUserInfo();
    })
}

function Like(){
  http.post("/reaction/like/",{'obj':'paper'+paper.id})
  .then(res=>{
    paper.like=res.data.like;
    paper.like_num=res.data.like_num;
  })
}

function ClipUrl(){
  Clip(window.location.href,"文章链接已复制OvO");
}

const router = useRouter();
const route = useRoute();
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
    <router-link :to="'/user/' + paper.user.id"
      style="display: flex;align-items: center;color:#809BA8;text-decoration: none;">
      <n-avatar :src="paper.user.avatar" />
      <span style="margin-left: 4px;">
        <div style="font-size: 16px;">{{ paper.user.nickname }}</div>
        <div style="margin-top: -4px;font-size:14px;">最后编辑于{{ paper.update_time }}</div>
      </span>
    </router-link>

    <n-space style="margin-top:4px">
      <n-button @click="Like" icon-placement="right"  color="#fb7299"
        :ghost="!paper.like">
        <template #icon>
          <n-icon>
            <ThumbUpFilled v-if="paper.like" />
            <ThumbUpOutlined v-else />
          </n-icon>
        </template>
        {{paper.like_num}}人赞同
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
    <n-divider style="color:#809BA8;font-size:14px;"><n-button @click="router.push('/paper/edit/'+paper.id)" icon-placement="right" text>
        <template #icon>
          <n-icon>
            <EditOutlined />
          </n-icon>
        </template>
        编辑此篇Paper
      </n-button></n-divider>
    <div style="color:#809BA8;">
      <div style="font-size:14px;"></div>
      
    </div>
  </div>
</template>