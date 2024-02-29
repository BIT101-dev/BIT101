<!--
 * @Author: flwfdd
 * @Date: 2022-07-17 01:40:53
 * @LastEditTime: 2024-02-26 16:54:04
 * @Description: 评论模块
 * _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import { h, onMounted, reactive, ref } from 'vue';
import MessageOutlined from '@vicons/material/MessageOutlined'
import ThumbUpOutlined from '@vicons/material/ThumbUpOutlined'
import ThumbUpFilled from '@vicons/material/ThumbUpFilled'
import DeleteOutlined from '@vicons/material/DeleteOutlined'
import ReplyOutlined from '@vicons/material/ReplyOutlined'
import FeedbackOutlined from '@vicons/material/FeedbackOutlined'
import MoreVertOutlined from '@vicons/material/MoreVertOutlined'
import store from '@/utils/store';
import { FormatTime } from '@/utils/tools';
import { onBeforeRouteLeave, useRouter } from 'vue-router';
import { Comment, User } from '@/utils/types';
import RenderLink from './RenderLink.vue';
import { UploadFileInfo, NIcon } from 'naive-ui';
import ImageViewer from "@/components/ImageViewer/ImageViewer.vue"


const props = defineProps(['obj', 'rate'])
const router = useRouter()

// 发表评论
const now_comment = reactive({
  text: '',
  anonymous: false,
  loading: false,
  with_image: false,
  rate: 5,
})

// 回复评论
const sub_comment = reactive({
  modal: false,
  parent: {} as Comment,
  reply_user: {} as User,
  reply_obj: '',
})

const comments = reactive({
  order: 'default',
  page: 0,
  end: false,
  list: [] as Comment[],
  loading: false,
})

const sub_comments = reactive({
  modal: false,
  parent: {} as Comment,
  order: 'old',
  page: 0,
  end: false,
  list: [] as Comment[],
  loading: false,
})

// 上传图片
const fileList = ref<UploadFileInfo[]>([])
const upload_url = store.api_url + "/upload/image";
const upload_head = {
  'fake-cookie': store.fake_cookie
}

function UploadHandler({ file, event }: { file: UploadFileInfo, event: ProgressEvent }) {
  let res = (event.target as XMLHttpRequest);
  let data = JSON.parse(res.response);
  file.name = data.mid;
  window.$message.success("上传成功OvO");
}

function UploadErrorHandler({ file, event }: { file: UploadFileInfo, event: ProgressEvent }) {
  let res = JSON.parse((event.target as XMLHttpRequest).response);
  if (res && res.msg) {
    window.$message.error(res.msg);
  }
}

const image_remove_modal = ref(false);
let ConfirmRemoveImage: (res: boolean) => void;
function OnImageRemove() {
  let promise = new Promise((resolve, reject) => {
    ConfirmRemoveImage = (res) => {
      if (res) resolve('');
      else reject();
      image_remove_modal.value = false
    }
  })
  image_remove_modal.value = true;
  return promise;
}

function Check() {
  if (now_comment.with_image == false && fileList.value.length == 0 && now_comment.text.length == 0) {
    window.$message.error('评论不能为空Orz');
    return false;
  }
  if (now_comment.with_image == false) {
    fileList.value = [];
  }
  return true;
}

function CommentPost(obj: string, parent_list: Comment[], reply_uid = 0, reply_obj = '') {
  if (!Check()) return;
  now_comment.loading = true;
  http.post("/reaction/comments", {
    obj: obj,
    text: now_comment.text,
    anonymous: now_comment.anonymous,
    reply_uid: reply_uid,
    reply_obj: reply_obj,
    rate: props.rate ? Math.round(now_comment.rate * 2) : 0,
    image_mids: fileList.value.map(i => i.name),
  }).then(res => {
    parent_list.unshift(res.data);
    now_comment.text = "";
    fileList.value = [];
    now_comment.anonymous = false;
    now_comment.loading = false;
    now_comment.rate = 5;
    sub_comment.modal = false;
    sub_comments.modal = false;
    window.$message.success('评论成功OvO');
  }).catch(() => {
    now_comment.loading = false;
  })
}

function OpenReplyModal(parent: Comment, reply_user = { 'id': 0 } as User, reply_obj = '') {
  sub_comment.modal = true;
  sub_comment.parent = parent;
  sub_comment.reply_user = reply_user;
  sub_comment.reply_obj = reply_obj;
  now_comment.rate = 0;
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
  sub_comments.parent = parent;
  sub_comments.page = 0;
  sub_comments.end = false;
  sub_comments.list = [];
  sub_comments.modal = true;
  LoadComments('comment' + parent.id, sub_comments);
}


const like_loading = reactive({} as Map<number, boolean>);
function Like(i: Comment) {
  like_loading[i.id] = true;
  http.post("/reaction/like", { 'obj': 'comment' + i.id })
    .then(res => {
      i.like = res.data.like;
      i.like_num = res.data.like_num;
      like_loading[i.id] = false;
    }).catch(() => { like_loading[i.id] = false; })
}

function Delete(i: any, cmts: any) {
  http.delete("/reaction/comments/" + i.id)
    .then(() => {
      cmts.list = cmts.list.filter((x: any) => (x.id != i.id))
    })
}

function renderIcon(icon: any) {
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

onMounted(() => {
  LoadComments(props.obj, comments);
})

onBeforeRouteLeave((to, from) => {
  sub_comments.modal = false;
})
</script>

<template>
  <n-space vertical>
    <n-rate v-if="props.rate" v-model:value="now_comment.rate" allow-half size="large" />
    <n-input v-model:value="now_comment.text" type="textarea" placeholder="沉默不是金" :autosize="{ minRows: 3 }"
      maxlength="23333" show-count />
    <n-upload v-show="now_comment.with_image" list-type="image-card" :action="upload_url" :headers="upload_head"
      @finish="UploadHandler" @error="UploadErrorHandler" :max="1" v-model:file-list="fileList"
      :on-remove="OnImageRemove" />
    <n-space justify="space-between">
      <n-space>
        <n-button @click="now_comment.with_image = !now_comment.with_image" ghost>附图:{{ now_comment.with_image ? '是'
          : '否' }}</n-button>
        <n-button @click="now_comment.anonymous = !now_comment.anonymous" ghost>匿名:{{ now_comment.anonymous ? '是'
          : '否' }}</n-button>
      </n-space>
      <n-button @click="CommentPost(props.obj, comments.list)" type="info" ghost :disabled="now_comment.loading"
        :loading="now_comment.loading" icon-placement="right">
        <template #icon>
          <n-icon>
            <MessageOutlined />
          </n-icon>
        </template>
        发表评论
      </n-button>
    </n-space>
  </n-space>


  <!-- 主评论列表 -->
  <template v-for="i in comments.list" :key="i.id">
    <n-divider></n-divider>
    <div style="display: flex;align-items: top;">
      <div>
        <router-link :to="'/user/' + i.user.id">
          <Avatar :user="i.user" :size="36" round />
        </router-link>
      </div>
      <span style="margin-left: 4px;margin-top:-4px;width:0;flex:1;">
        <div style="font-size: 16px;">{{ i.user.nickname }}</div>
        <div style="margin-top: -4px;font-size:14px;">{{ FormatTime(i.create_time) }}</div>
        <n-rate v-if="props.rate" :value="i.rate / 2" allow-half size="large" readonly />
        <div style="white-space:pre-wrap;margin-top:4px;word-wrap:break-word;">
          <RenderLink :value="i.text" />
        </div>
        <ImageViewer v-if="i.images.length > 0" :images="i.images" />
        <n-space :align="'center'">
          <n-button @click="Like(i)" color="#fb7299" text :loading="like_loading[i.id]" :disabled="like_loading[i.id]">
            <template #icon>
              <n-icon>
                <ThumbUpFilled v-if="i.like" />
                <ThumbUpOutlined v-else />
              </n-icon>
            </template>
            {{ i.like_num }}赞同
          </n-button>

          <n-button @click="OpenReplyModal(i)" text>
            <template #icon>
              <n-icon :component="ReplyOutlined" />
            </template>
            回复
          </n-button>

          <n-popconfirm @positive-click="Delete(i, comments)" :show-icon="false" positive-text="确定" negative-text="取消">
            <template #trigger>
              <n-button v-show="i.own" text>
                <template #icon>
                  <n-icon :component="DeleteOutlined" />
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
  <n-divider style="color:var(--text-color-3);font-size:14px;">已加载{{ comments.list.length }}条</n-divider>
  <n-button block @click="LoadComments(props.obj, comments)" :disabled="comments.end" :loading="comments.loading">
    {{ comments.end ? '木有更多了' : '加载更多' }}</n-button>

  <!-- 回复模态框 -->
  <n-modal v-model:show="sub_comment.modal" preset="card" style="width:624px"
    :title="'回复' + (sub_comment.reply_user.id == 0 ? '' : '@' + sub_comment.reply_user.nickname)">
    <n-space vertical>
      <n-input v-model:value="now_comment.text" type="textarea" placeholder="沉默不是金" :autosize="{ minRows: 3 }"
        maxlength="23333" show-count />
      <n-upload v-show="now_comment.with_image" list-type="image-card" :action="upload_url" :headers="upload_head"
        @finish="UploadHandler" @error="UploadErrorHandler" :max="1" v-model:file-list="fileList"
        :on-remove="OnImageRemove" />
      <n-space justify="space-between">
        <n-space>
          <n-button @click="now_comment.with_image = !now_comment.with_image" ghost>附图:{{ now_comment.with_image ? '是'
            : '否' }}</n-button>
          <n-button @click="now_comment.anonymous = !now_comment.anonymous" ghost>匿名:{{ now_comment.anonymous ? '是'
            : '否' }}</n-button>
        </n-space>
        <n-button
          @click="CommentPost('comment' + sub_comment.parent.id, sub_comment.parent.sub, sub_comment.reply_user.id, sub_comment.reply_obj)"
          type="info" ghost :disabled="now_comment.loading" :loading="now_comment.loading" icon-placement="right">
          <template #icon>
            <n-icon>
              <ReplyOutlined />
            </n-icon>
          </template>
          回复
        </n-button>
      </n-space>
    </n-space>
  </n-modal>

  <!-- 子评论模态框 -->
  <n-modal v-model:show="sub_comments.modal" preset="card" style="width:624px">
    <n-scrollbar style="max-height:84vh">
      <div style="display: flex;align-items: top;">

        <!-- 子评论的父评论 -->
        <div>
          <router-link :to="'/user/' + sub_comments.parent.user.id">
            <Avatar :user="sub_comments.parent.user" :size="36" round />
          </router-link>
        </div>
        <span style="margin-left: 4px;margin-top:-4px">
          <div style="font-size: 16px;">{{ sub_comments.parent.user.nickname }}</div>
          <div style="margin-top: -4px;font-size:14px;">{{ FormatTime(sub_comments.parent.create_time) }}</div>
          <div style="white-space:pre-wrap;margin-top:4px;word-wrap:break-word;">
            <RenderLink :value="sub_comments.parent.text" />
          </div>
          <ImageViewer v-if="sub_comments.parent.images.length > 0" :images="sub_comments.parent.images" />
        </span>
      </div>

      <!-- 子评论列表 -->
      <template v-for="i in sub_comments.list" :key="i.id">
        <n-divider style="margin:11px"></n-divider>
        <div style="display: flex;align-items: top;">
          <div>
            <router-link :to="'/user/' + i.user.id">
              <Avatar :user="i.user" :size="36" round />
            </router-link>
          </div>
          <span style="margin-left: 4px;margin-top:-4px">
            <div style="font-size: 16px;">{{ i.user.nickname }}</div>
            <div style="margin-top: -4px;font-size:14px;">{{ FormatTime(i.create_time) }}</div>
            <div style="white-space: pre-wrap;margin-top:4px;word-wrap:break-word;">
              <n-a v-if="i.reply_user.id != 0" :href="'/user/' + i.reply_user.id" style="text-decoration:none;">
                @{{ i.reply_user.nickname + ' ' }}
              </n-a>
              <RenderLink :value="i.text" />
            </div>
            <ImageViewer v-if="i.images.length > 0" :images="i.images" />

            <n-space :align="'center'">
              <n-button @click="Like(i)" color="#fb7299" text :loading="like_loading[i.id]"
                :disabled="like_loading[i.id]">
                <template #icon>
                  <n-icon>
                    <ThumbUpFilled v-if="i.like" />
                    <ThumbUpOutlined v-else />
                  </n-icon>
                </template>
                {{ i.like_num }}赞同
              </n-button>

              <n-button @click="OpenReplyModal(sub_comments.parent, i.user, 'comment' + i.id)" text>
                <template #icon>
                  <n-icon>
                    <ReplyOutlined />
                  </n-icon>
                </template>
                回复
              </n-button>

              <n-popconfirm @positive-click="Delete(i, sub_comments)" :show-icon="false" positive-text="确定"
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
          </span>
        </div>
      </template>
      <n-divider style="color:var(--text-color-3);font-size:14px;">已加载{{ sub_comments.list.length }}条</n-divider>
      <n-button block @click="LoadComments('comment' + sub_comments.parent.id, sub_comments)" :disabled="sub_comments.end"
        :loading="sub_comments.loading">
        {{ sub_comments.end ? '木有更多了' : '加载更多' }}</n-button>
    </n-scrollbar>
  </n-modal>


  <!-- 删除图片确认 -->
  <n-modal v-model:show="image_remove_modal" preset="dialog" title="汝真断舍离耶？" positive-text="确认" negative-text="取消"
    @positive-click="ConfirmRemoveImage(true)" @negative-click="ConfirmRemoveImage(false)" />
</template>