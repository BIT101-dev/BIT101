<!--
 * @Author: flwfdd
 * @Date: 2023-10-20 21:27:17
 * @LastEditTime: 2024-02-26 16:36:33
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import store from '@/utils/store';
import { onMounted, ref, watch, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { FormatTime, setTitle } from '@/utils/tools';
import { Poster } from '@/utils/types';
import { UploadFileInfo, AutoCompleteInst, useMessage } from 'naive-ui';

const route = useRoute();
const router = useRouter();

// 初始化数据
const draftData = store.last_draft[router.currentRoute.value.fullPath]
console.debug(draftData)
const hasDraft = ref(!!draftData);

const BLANK_POSTER = JSON.stringify({
  id: 0,
  title: "",
  text: "",
  claim: {
    id: 0,
    text: "",
  },
  anonymous: false,
  public: true,
  plugins: "[]",
  tags: [] as string[],
} as Poster)
const poster = ref<Poster>(JSON.parse(BLANK_POSTER))

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

// 设置Tag
const autoCompleteInstRef = ref<AutoCompleteInst | null>(null)
watch(autoCompleteInstRef, (value) => {
  updateTag()
  if (value) nextTick(() => value.focus())
})

const rawTag = ref("")
const rawTagLengthLimit = ref("" as "error" | undefined)
const tags = ref([] as { label: string, value: string }[])
watch(rawTag, updateTag)

async function updateTag() {
  if (rawTag.value !== null && rawTag.value.length > 11) {
    rawTagLengthLimit.value = "error"
    return ;
  }
  rawTagLengthLimit.value = undefined
  
  if (rawTag.value === "" || rawTag.value === null) {
    // let { data } = await http.get<string[]>(**推荐tag api**)
    let data = ["水", "活动", "表白", "树洞", "求助", "聊天", "抽象"]
    tags.value = data.map((tag) => { return { label: tag, value: tag } })
    return ;
  }

  let data = ["水", "活动", "表白", "树洞", "求助", "聊天", "抽象"]
  // let { data } = await http.get<string[]>(**tag api**)

  let exactMatched = false
  let matchedTags = data.map((tag) => {
    if (tag === rawTag.value) exactMatched = true
    if (tag.indexOf(rawTag.value) !== -1) return { label: tag, value: tag }
  }).filter(item => item !== undefined) as { label: string, value: string }[]

  // 将用户输入项放在首位 方便直接选择
  if (!exactMatched) matchedTags.unshift({ label: rawTag.value, value: rawTag.value })
  tags.value = matchedTags
  return
}

// 声明
const claims = ref([] as { label: number, value: string }[]);
function LoadClaims() {
  http.get("/posters/claims")
    .then(res => {
      claims.value = res.data.map((i: any) => { return { label: i.text, value: i.id } });
    })
}

//加载帖子
function LoadPoster() {
  return http.get("/posters/" + poster.value.id)
    .then(res => {
      poster.value = res.data;
      fileList.value = poster.value.images.map(i => { return { id: i.mid, name: i.mid, status: 'finished', url: i.url } })
    })
}


// 检查信息
function Check() {
  if (poster.value.title.length == 0) {
    window.$message.error("标题不能为空Orz");
    return false;
  }
  if (poster.value.text.length == 0) {
    window.$message.error("内容不能为空Orz");
    return false;
  }
  if (poster.value.tags.length < 2) {
    window.$message.error("标签不能少于2个Orz");
    return false;
  }
  let tags = new Set(poster.value.tags);
  if (tags.size != poster.value.tags.length) {
    window.$message.error("标签不能重复Orz");
    return false;
  }
  return true;
}


// 发布帖子
const posting = ref(false);
function PostPoster() {
  if (!Check()) return;
  posting.value = true;

  let poster_data = {
    title: poster.value.title,
    text: poster.value.text,
    image_mids: fileList.value.map(i => i.name),
    plugins: poster.value.plugins,
    anonymous: poster.value.anonymous,
    tags: poster.value.tags,
    claim_id: poster.value.claim.id,
    public: poster.value.public,
  }

  if (poster.value.id == 0) {
    http.post("/posters", poster_data).then((res) => {
      posting.value = false;
      router.replace('/gallery/' + res.data.id);
    }).catch(() => {
      posting.value = false;
    })
  } else {
    http.put("/posters/" + poster.value.id, poster_data).then(() => {
      posting.value = false;
      router.go(-1);
    }).catch(() => {
      posting.value = false;
    })
  }
}

const draft_use_modal = ref(false);
let ConfirmUseDraft: (res: boolean) => void;
const OnUseDraft = () => {
  draft_use_modal.value = true;
  return new Promise<null>((resolve, reject) => {
    ConfirmUseDraft = (res) => {
      draft_use_modal.value = false;
      if (res) resolve(null)
      else reject()
    }
  })
}

const original = ref<Poster>();
const DiscardDraft = () => {
  delete store.last_draft[router.currentRoute.value.fullPath];
  if (original.value) {
    poster.value = original.value;
  }
  else {
    poster.value = JSON.parse(BLANK_POSTER);
  }
  hasDraft.value = false;
}

watch(() => poster.value, () => {
  if (JSON.stringify(poster.value) === BLANK_POSTER) return;
  store.last_draft[router.currentRoute.value.fullPath] = {
    poster: JSON.stringify(poster.value),
    timestamp: Date.now()
  };
}, { deep: true })

onMounted(async () => {
  LoadClaims();
  poster.value.id = Number(route.params.id);
  const isCreate = poster.value.id == 0;
  if (isCreate) {
    setTitle('发布', '话廊');
    if (hasDraft.value) {
      poster.value = JSON.parse(draftData.poster);
      window.$message.success(`已恢复 ${FormatTime(draftData.timestamp / 1000)} 的草稿 OvO`);
    }
  }
  else {
    await LoadPoster()
    if (hasDraft.value) {
      original.value = poster.value;
      OnUseDraft().then(() => {
        poster.value = JSON.parse(draftData.poster);
        window.$message.success(`已恢复 ${FormatTime(draftData.timestamp / 1000)} 的草稿 OvO`);
      }).catch(() => {
        DiscardDraft()
      })
    }
    setTitle('编辑', '话廊');
  }
})

</script>

<template>
  <div class="container">
    <n-space vertical size="large">
      <n-h2 style="margin-top:0px;margin-bottom:-6px;">🌟 {{ poster.id == 0 ? '发布 Poster' : '编辑 Poster ' }}</n-h2>

      <n-space vertical size="small">
        <div>标题</div>
        <n-input v-model:value="poster.title" placeholder="请输入标题" maxlength="42" show-count></n-input>
      </n-space>

      <n-space vertical size="small">
        <div>内容</div>
        <n-input v-model:value="poster.text" type="textarea" placeholder="请输入内容" :autosize="{ minRows: 6 }"
          maxlength="23333" show-count />
      </n-space>

      <n-space vertical size="small">
        <div>图片</div>
        <n-upload list-type="image-card" :action="upload_url" :headers="upload_head" @finish="UploadHandler"
          @error="UploadErrorHandler" :max="9" v-model:file-list="fileList" :on-remove="OnImageRemove" />
      </n-space>

      <n-space vertical size="small">
        <div>标签</div>
        <div style="color:var(--text-color-3);font-size:14px;margin-top:-6px;">请至少添加2个标签，合适的标签将有助于内容推荐。</div>
        <n-dynamic-tags v-model:value="poster.tags">
          <template #input="{ submit, deactivate }">
            <n-auto-complete ref="autoCompleteInstRef" v-model:value="rawTag" size="small" :clear-after-select="true"
              :options="tags" @select="($event: any) => { submit($event); deactivate() }"
              @blur="() => { deactivate(); rawTag = ''; }" placeholder="选一个吧，或者输入你想要的" :get-show="() => true"
              :status="rawTagLengthLimit" />
          </template>
        </n-dynamic-tags>
      </n-space>

      <n-space vertical size="small">
        <div>声明</div>
        <div style="color:var(--text-color-3);font-size:14px;margin-top:-6px;">请根据社区公约选择合适的声明，否则可能会被制裁。</div>
        <n-select v-model:value="poster.claim.id" :options="claims" />
      </n-space>

      <n-space>
        <n-button @click="poster.anonymous = !poster.anonymous" ghost>匿名:{{ poster.anonymous ? '是' : '否' }}</n-button>
        <n-button @click="poster.public = !poster.public" ghost>公开:{{ poster.public ? '是' : '否' }}</n-button>
      </n-space>

      <n-space justify="end">
        <n-popconfirm v-if="hasDraft" @positive-click="DiscardDraft" positive-text="确定" negative-text="取消">
          <template #trigger>
            <n-button type="error" ghost>放弃草稿</n-button>
          </template>
          汝真放弃耶？放弃的草稿无法恢复。
        </n-popconfirm>
        <n-popconfirm @positive-click="PostPoster" :show-icon="false" positive-text="确定" negative-text="取消">
          <template #trigger>
            <n-button :disabled="posting" type="success" ghost>张贴Poster</n-button>
          </template>
          汝真发布耶？
        </n-popconfirm>
      </n-space>

    </n-space>

    <n-modal v-model:show="image_remove_modal" preset="dialog" title="汝真断舍离耶？" positive-text="确认" negative-text="取消"
      @positive-click="ConfirmRemoveImage(true)" @negative-click="ConfirmRemoveImage(false)" />

    <n-modal v-if="hasDraft" v-model:show="draft_use_modal" preset="dialog" title="要对 话廊 使用 草稿 吗？"
      :content="`现有一个 ${FormatTime(draftData.timestamp / 1000)} 的草稿, 放弃后无法恢复`"
      positive-text="使用" negative-text="放弃" :closable="false" :closeOnEsc="false" :maskClosable="false"
      @positive-click="ConfirmUseDraft(true)" @negative-click="ConfirmUseDraft(false)" />
  </div>
</template>