<!--
 * @Author: flwfdd
 * @Date: 2023-10-20 21:27:17
 * @LastEditTime: 2023-10-21 16:10:33
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import store from '@/utils/store';
import { onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { setTitle } from '@/utils/tools';
import { Image, Poster } from '@/utils/types';
import { AddRound } from '@vicons/material';
import { UploadFileInfo } from 'naive-ui';

const route = useRoute();
const router = useRouter();

// 初始化数据
const poster = ref({
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

//发表帖子
function Check() {
  if (poster.value.title.length == 0) {
    window.$message.error("标题不能为空Orz");
    return false;
  }
  if (poster.value.text.length == 0) {
    window.$message.error("内容不能为空Orz");
    return false;
  }
  if (poster.value.tags.length < 3) {
    window.$message.error("标签不能少于3个Orz");
    return false;
  }
  return true;
}

const posting = ref(false);
function PostPoster() {
  if(!Check())return;
  console.log(fileList.value);
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
      router.push('/gallery/' + res.data.id);
    }).catch(() => {
      posting.value = false;
    })
  } else {
    http.put("/posters/" + poster.value.id, poster_data).then(() => {
      posting.value = false;
      router.push('/gallery/' + poster.value.id);
    }).catch(() => {
      posting.value = false;
    })
  }
}

onMounted(async () => {
  LoadClaims();
  poster.value.id = Number(route.params.id);
  if (poster.value.id == 0) setTitle('发布', '话廊');
  else {
    await LoadPoster()
    setTitle('编辑', '话廊');
  }
})

</script>

<template>
  <div class="container">
    <n-space vertical size="large">
      <h2 style="color:#00BCD4;margin-top:0px;margin-bottom:-6px;">🌟 {{ poster.id == 0 ? '发布 Poster' : '编辑 Poster ' }}</h2>

      <n-space vertical size="small">
        <div>标题</div>
        <n-input v-model:value="poster.title" placeholder="请输入标题" maxlength="42" show-count></n-input>
      </n-space>

      <n-space vertical size="small">
        <div>内容</div>
        <n-input v-model:value="poster.text" type="textarea" placeholder="请输入内容" :autosize="{ minRows: 6 }" />
      </n-space>

      <n-space vertical size="small">
        <div>图片</div>
        <n-upload list-type="image-card" :action="upload_url" :headers="upload_head" @finish="UploadHandler" :max="9"
          v-model:file-list="fileList" :on-remove="OnImageRemove" />
      </n-space>

      <n-space vertical size="small">
        <div>标签</div>
        <div style="color:#809BA8;font-size:14px;margin-top:-6px;">请至少添加3个标签，合适的标签将有助于内容推荐。</div>
        <n-dynamic-tags v-model:value="poster.tags" :input-props="{ 'maxlength': 11, 'show-count': true }" />
      </n-space>

      <n-space vertical size="small">
        <div>声明</div>
        <div style="color:#809BA8;font-size:14px;margin-top:-6px;">请根据社区公约选择合适的声明，否则可能会被制裁。</div>
        <n-select v-model:value="poster.claim.id" :options="claims" />
      </n-space>

      <n-space>
        <n-button @click="poster.anonymous = !poster.anonymous" ghost>匿名:{{ poster.anonymous ? '是' : '否' }}</n-button>
        <n-button @click="poster.public = !poster.public" ghost>公开:{{ poster.public ? '是' : '否' }}</n-button>
      </n-space>

      <n-space justify="end">
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
  </div>
</template>