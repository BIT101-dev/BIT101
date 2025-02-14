<template>
  <n-space vertical>
    <n-rate v-if="props.rate && !props.subcomment" v-model:value="now_comment.rate" allow-half size="large" />
    <n-input v-model:value="now_comment.text" type="textarea" placeholder="沉默不是金" :autosize="{ minRows: 3 }"
      maxlength="23333" show-count />
    <n-upload v-show="now_comment.with_image" list-type="image-card" :action="upload_url" :headers="upload_head"
      @finish="UploadHandler" @error="UploadErrorHandler" v-model:file-list="fileList" :on-remove="OnImageRemove" />
    <n-space justify="space-between">
      <n-space>
        <n-button @click="now_comment.with_image = !now_comment.with_image" ghost>
          附图:{{ now_comment.with_image ? '是' : '否' }}
        </n-button>
        <n-button @click="now_comment.anonymous = !now_comment.anonymous" ghost>
          匿名:{{ now_comment.anonymous ? '是' : '否' }}
        </n-button>
      </n-space>
      <n-space>
        <n-popconfirm v-if="hasDraft" @positive-click="DiscardDraft" positive-text="确定" negative-text="取消">
          <template #trigger>
            <n-button type="error" ghost>放弃草稿</n-button>
          </template>
          汝真放弃耶？放弃的草稿无法恢复。
        </n-popconfirm>
        <n-button @click="CommentPost(
          props.target,
          props.parent_list,
          props.reply_uid,
          props.reply_obj
        )" type="info" ghost :disabled="now_comment.loading" :loading="now_comment.loading" icon-placement="right">
          <template #icon>
            <n-icon>
              <MessageOutlined v-if="!props.subcomment" />
              <ReplyOutlined v-else />
            </n-icon>
          </template>
          {{ props.subcomment ? "回复" : "发表评论" }}
        </n-button>
      </n-space>
    </n-space>
  </n-space>

  <!-- 删除图片确认 -->
  <n-modal v-model:show="image_remove_modal" preset="dialog" title="汝真断舍离耶？" positive-text="确认" negative-text="取消"
    @positive-click="ConfirmRemoveImage(true)" @negative-click="ConfirmRemoveImage(false)" />
</template>

<script lang="ts" setup>
import http from '@/utils/request';
import store from '@/utils/store';
import { Comment } from '@/utils/types';
import { UploadFileInfo } from 'naive-ui';
import { onMounted, reactive, ref, watch } from 'vue';
import { useRouter } from 'vue-router';

import MessageOutlined from '@vicons/material/MessageOutlined';
import ReplyOutlined from '@vicons/material/ReplyOutlined';
import { FormatTime } from '@/utils/tools';
import { computed } from 'vue';

const router = useRouter();

const props = defineProps({
  subcomment: {
    type: Boolean,
    default: false
  },
  rate: {
    type: Boolean,
    default: false
  },
  target: {
    type: String,
    required: true
  },
  parent_list: {
    type: Array<Comment>,
    required: true
  },
  reply_uid: {
    type: Number,
    default: 0
  },
  reply_obj: {
    type: String,
    default: ''
  }
})

const emits = defineEmits<{
  closeReply: [],
  closeSubComments: [],
}>()

// 发表评论
const now_comment = reactive<{
  text: string,
  anonymous: boolean,
  loading: boolean,
  with_image: boolean,
  rate: number,
}>(store.last_draft[router.currentRoute.value.fullPath] ?? {
  text: '',
  anonymous: false,
  loading: false,
  with_image: false,
  rate: 5,
})

// 上传图片
const fileList = ref<UploadFileInfo[]>([])
const upload_url = store.api_url + "/upload/image";
const upload_head = {
  'fake-cookie': store.fake_cookie
}

const Check = () => {
  if (now_comment.with_image == false && fileList.value.length == 0 && now_comment.text.length == 0) {
    window.$message.error('评论不能为空Orz');
    return false;
  }
  if (now_comment.with_image == false) {
    fileList.value = [];
  }
  return true;
}

const CommentPost = (obj: string, parent_list: Comment[], reply_uid = 0, reply_obj = '') => {
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
    now_comment.with_image = false;
    now_comment.loading = false;
    now_comment.rate = 5;
    emits("closeReply");
    emits("closeSubComments");
    window.$message.success('评论成功OvO');
  }).catch(() => {
    now_comment.loading = false;
  })
}

const UploadHandler = ({ file, event }: { file: UploadFileInfo, event: ProgressEvent }) => {
  let res = (event.target as XMLHttpRequest);
  let data = JSON.parse(res.response);
  file.name = data.mid;
  window.$message.success("上传成功OvO");
}

const UploadErrorHandler = ({ file, event }: { file: UploadFileInfo, event: ProgressEvent }) => {
  let res = JSON.parse((event.target as XMLHttpRequest).response);
  if (res && res.msg) {
    window.$message.error(res.msg);
  }
}

const image_remove_modal = ref(false);
let ConfirmRemoveImage: (res: boolean) => void;
const OnImageRemove = () => {
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

watch(now_comment, () => {
  if (now_comment.text.length) {
    store.last_draft[props.target] = {
      ...now_comment,
      timestamp: Date.now()
    }
  }
  else {
    DiscardDraft();
  }
})

const DiscardDraft = () => {
  now_comment.text = "";
  if (store.last_draft[props.target])
    delete store.last_draft[props.target];

  hasDraft.value = false;
}

const draftComment = computed(() => {
  return store.last_draft[props.target]
})

const hasDraft = ref(!!draftComment.value);

onMounted(() => {
  if (hasDraft.value) {
    now_comment.text = draftComment.value.text;
    now_comment.anonymous = draftComment.value.anonymous;
    now_comment.with_image = draftComment.value.with_image;
    now_comment.rate = draftComment.value.rate;

    window.$message.success(`已恢复 ${FormatTime(draftComment.value.timestamp / 1000)} 的草稿 OvO`);
  }
})
</script>