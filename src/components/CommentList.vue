<template>
  <template v-for="i in props.ctx.list" :key="i.id">
    <n-divider :style="`margin:${subcomment ? 11 : 24}px`"></n-divider>
    <div style="display: flex;align-items: top;">
      <div>
        <router-link :to="'/user/' + i.user.id">
          <Avatar :user="i.user" :size="36" round />
        </router-link>
      </div>
      <span style="margin-left: 4px;margin-top:-4px;flex:1">
        <div style="font-size: 16px;">{{ i.user.nickname }}</div>
        <div style="margin-top: -4px;font-size:14px;">{{ FormatTime(i.create_time) }}</div>
        <n-rate v-if="props.rate && !props.subcomment" :value="i.rate / 2" allow-half size="large" readonly />
        <div style="white-space: pre-wrap;margin-top:4px;word-wrap:break-word;">
          <n-a v-if="i.reply_user.id != 0" :href="'/user/' + i.reply_user.id" style="text-decoration:none;">
            @{{ i.reply_user.nickname + ' ' }}
          </n-a>
          <RenderLink :value="i.text" />
        </div>
        <ImageViewer v-if="i.images.length > 0" :images="i.images" />

        <n-space :align="'center'">
          <n-button @click="Like(i)" color="#fb7299" text :loading="like_loading.get(i.id)"
            :disabled="like_loading.get(i.id)">
            <template #icon>
              <n-icon>
                <ThumbUpFilled v-if="i.like" />
                <ThumbUpOutlined v-else />
              </n-icon>
            </template>
            {{ i.like_num }}赞同
          </n-button>

          <n-button text @click="() => (props.ctx.parent)
              ? OpenReplyModal(props.ctx.parent, i.user, 'comment' + i.id)
              : OpenReplyModal(i)">
            <template #icon>
              <n-icon>
                <ReplyOutlined />
              </n-icon>
            </template>
            回复
          </n-button>

          <n-popconfirm @positive-click="Delete(i, props.ctx)" :show-icon="false" positive-text="确定"
            negative-text="取消">
            <template #trigger>
              <n-button v-show="i.own" text>
                <template #icon>
                  <n-icon>
                    <DeleteOutlined />
                  </n-icon>
                </template>
                删除
              </n-button>
            </template>
            汝真断舍离耶？
          </n-popconfirm>

          <n-dropdown :options="dropdown.options" trigger="click">
            <div style="display:flex;align-items: center;">
              <n-button @click="dropdown.comment = i" text>
                <template #icon>
                  <n-icon :component="MoreVertOutlined" />
                </template>
              </n-button>
            </div>
          </n-dropdown>
        </n-space>

        <!-- 子评论预览 -->
        <div v-if="i.sub.length != 0" style="background-color:#CCCCCC22;padding:4px;border-radius: 4px;">
          <div v-for="j in i.sub.slice(0, 3)" :key="j.id" style="margin:4px;">
            {{ j.user.nickname }}：
            <span v-if="j.reply_user.id != 0">@{{ j.reply_user.nickname + ' ' }}</span>
            <span style="white-space:pre-wrap;margin-top:4px;word-wrap:break-word;">{{ (j.images.length ? '【图片】' : '') +
              j.text
              }}</span>
          </div>
          <n-button @click="OpenSubComments(i)" text>共{{ i.comment_num }}条回复>></n-button>
        </div>
      </span>
    </div>
  </template>
</template>

<script setup lang="tsx">
import { FormatTime } from '@/utils/tools';
import { PropType, reactive, ref } from 'vue';
import http from '@/utils/request';
import { Comment, CommentList, User } from '@/utils/types';
import { NIcon } from 'naive-ui';
import { h } from 'vue';
import { useRouter } from 'vue-router';

import MoreVertOutlined from '@vicons/material/MoreVertOutlined';
import FeedbackOutlined from '@vicons/material/FeedbackOutlined';
import ThumbUpOutlined from '@vicons/material/ThumbUpOutlined'
import ThumbUpFilled from '@vicons/material/ThumbUpFilled'
import DeleteOutlined from '@vicons/material/DeleteOutlined'
import ReplyOutlined from '@vicons/material/ReplyOutlined'

const router = useRouter();

const props = defineProps({
  ctx: { type: Object as PropType<CommentList>, required: true },
  rate: { type: Boolean, default: false },
  subcomment: { type: Boolean, default: false },
})

const emits = defineEmits<{
  openReply: [parent: Comment, reply_user: User, reply_obj: string],
  openSubComments: [comm: Comment],
}>()

const like_loading = ref<Map<number, boolean>>(new Map());
const Like = (comm: Comment) => {
  like_loading.value.set(comm.id, true);
  http.post("/reaction/like", { 'obj': 'comment' + comm.id })
    .then(res => {
      comm.like = res.data.like;
      comm.like_num = res.data.like_num;
      like_loading.value.set(comm.id, false);
    }).catch(() => { like_loading.value.set(comm.id, false); })
}

const Delete = (i: any, cmts: any) => {
  http.delete("/reaction/comments/" + i.id)
    .then(() => {
      cmts.list = cmts.list.filter((x: any) => (x.id != i.id))
    })
}

const renderIcon = (icon: any) => {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const dropdown = reactive({
  comment: {} as Comment,
  options: [
    {
      label: '举报',
      key: 'report',
      icon: renderIcon(FeedbackOutlined),
      props: {
        onClick: () => {
          router.push('/report/comment' + dropdown.comment.id);
        }
      }
    },
  ]
})

const OpenReplyModal = (parent: Comment, reply_user = { 'id': 0 } as User, reply_obj = '') => {
  emits("openReply", parent, reply_user, reply_obj);
}

const OpenSubComments = (comm: Comment) => {
  emits("openSubComments", comm);
}
</script>
