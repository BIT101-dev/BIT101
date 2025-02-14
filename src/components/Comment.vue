<!--
 * @Author: flwfdd
 * @Date: 2022-07-17 01:40:53
 * @LastEditTime: 2024-02-26 16:54:04
 * @Description: 评论模块
 * _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import { h, onMounted, reactive } from 'vue';
import { FormatTime } from '@/utils/tools';
import { onBeforeRouteLeave } from 'vue-router';
import { Comment, CommentList as ICommentList, User } from '@/utils/types';
import RenderLink from './RenderLink.vue';
import ImageViewer from "@/components/ImageViewer/ImageViewer.vue"
import CommentList from './CommentList.vue';
import CommentEdit from './CommentEdit.vue';


const props = defineProps(['obj', 'rate'])

// 回复评论
const sub_comment = reactive({
  modal: false,
  parent: {} as Comment,
  reply_user: {} as User,
  reply_obj: '',
})

const comments = reactive<ICommentList>({
  order: 'default',
  page: 0,
  end: false,
  list: [] as Comment[],
  loading: false,
})

const sub_comment_list = reactive<ICommentList>({
  modal: false,
  parent: {} as Comment,
  order: 'old',
  page: 0,
  end: false,
  list: [] as Comment[],
  loading: false,
})

function OpenReplyModal(parent: Comment, reply_user = { 'id': 0 } as User, reply_obj = '') {
  sub_comment.modal = true;
  sub_comment.parent = parent;
  sub_comment.reply_user = reply_user;
  sub_comment.reply_obj = reply_obj;
}

function LoadComments(obj: string, cmts: any) {
  cmts.loading = true;
  http.get('/reaction/comments', {
    params: {
      obj: obj,
      order: cmts.order,
      page: cmts.page,
    }
  }).then(res => {
    if (res.data.length == 0) cmts.end = true;
    else {
      cmts.list = cmts.list.concat(res.data);
      cmts.page++;
    }
    cmts.loading = false;
  }).catch(() => { cmts.loading = false; })
}


function OpenSubComments(parent: any) {
  sub_comment_list.parent = parent;
  sub_comment_list.page = 0;
  sub_comment_list.end = false;
  sub_comment_list.list = [];
  sub_comment_list.modal = true;
  LoadComments('comment' + parent.id, sub_comment_list);
}

onMounted(() => {
  LoadComments(props.obj, comments);
})

onBeforeRouteLeave((to, from) => {
  sub_comment_list.modal = false;
  sub_comment.modal = false;
})
</script>

<template>
  <CommentEdit :target="props.obj" :rate="props.rate" :parent_list="comments.list"
    @close-reply="() => sub_comment.modal = false" />

  <!-- 主评论列表 -->
  <CommentList :ctx="comments" :rate="props.rate" @open-reply="OpenReplyModal" @open-sub-comments="OpenSubComments" />
  <n-divider style="color:var(--text-color-3);font-size:14px;">
    已加载{{ comments.list.length }}条
  </n-divider>
  <n-button block @click="LoadComments(props.obj, comments)" :disabled="comments.end" :loading="comments.loading">
    {{ comments.end ? '木有更多了' : '加载更多' }}
  </n-button>

  <!-- 回复模态框 -->
  <n-modal v-model:show="sub_comment.modal" preset="card" style="width:624px"
    :title="'回复' + (sub_comment.reply_user.id == 0 ? '' : '@' + sub_comment.reply_user.nickname)">
    <CommentEdit :subcomment="true" :target="`comment${sub_comment.parent.id}`"
      :parent_list="sub_comment.parent.sub"
      :reply_uid="sub_comment.reply_user.id" :reply_obj="sub_comment.reply_obj"
      @close-reply="() => sub_comment.modal = false"
      @close-sub-comments="() => sub_comment_list.modal = false" />
  </n-modal>

  <!-- 子评论模态框 -->
  <n-modal v-model:show="sub_comment_list.modal" preset="card" style="width:624px">
    <n-scrollbar style="max-height:84vh">
      <div style="display: flex;align-items: top;">

        <!-- 子评论的父评论 -->
        <div>
          <router-link :to="'/user/' + sub_comment_list.parent!.user.id">
            <Avatar :user="sub_comment_list.parent!.user" :size="36" round />
          </router-link>
        </div>

        <span style="margin-left: 4px;margin-top:-4px">
          <div style="font-size: 16px;">{{ sub_comment_list.parent!.user.nickname }}</div>
          <div style="margin-top: -4px;font-size:14px;">{{ FormatTime(sub_comment_list.parent!.create_time) }}</div>
          <div style="white-space:pre-wrap;margin-top:4px;word-wrap:break-word;">
            <RenderLink :value="sub_comment_list.parent!.text" />
          </div>
          <ImageViewer v-if="sub_comment_list.parent!.images.length > 0" :images="sub_comment_list.parent!.images" />
        </span>
      </div>

      <n-divider style="color:var(--text-color-3);font-size:14px;">
        现有{{ sub_comment_list.list.length }}条评论
      </n-divider>

      <!-- 子评论列表 -->
      <CommentList :ctx="sub_comment_list" subcomment @open-reply="OpenReplyModal" />
      <n-divider style="color:var(--text-color-3);font-size:14px;">已加载{{ sub_comment_list.list.length }}条</n-divider>
      <n-button block @click="LoadComments('comment' + sub_comment_list.parent!.id, sub_comment_list)"
        :disabled="sub_comment_list.end" :loading="sub_comment_list.loading">
        {{ sub_comment_list.end ? '木有更多了' : '加载更多' }}</n-button>
    </n-scrollbar>
  </n-modal>
</template>