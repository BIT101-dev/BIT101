<!--
 * @Author: flwfdd
 * @Date: 2022-06-01 14:21:01
 * @LastEditTime: 2023-10-20 18:30:24
 * @Description: 用户中心
 * _(:з」∠)_
-->
<script setup lang="ts">
import { FormatTime, hitokoto, setTitle } from '@/utils/tools';
import http from '@/utils/request';
import { onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';
import store from '@/utils/store';
import { UploadFileInfo } from 'naive-ui';
import { User } from '@/utils/types';
import Avatar from '@/components/Avatar.vue';

const user = ref({} as User);
function GetInfo(uid: any) {
  http.get("/user/info/" + uid)
    .then(res => {
      user.value = res.data.user;
      if (user.value.id) setTitle(user.value.nickname, "用户");
    })
}

const route = useRoute();
onMounted(() => {
  GetInfo(route.params.id);
})

const edit_info = reactive({
  model: false,
  avatar_mid: "",
  avatar_url: "",
  nickname: "",
  motto: ""
})

const upload_url = store.api_url + "/upload/image";
const upload_head = {
  'fake-cookie': store.fake_cookie
}

function UploadHandler({ file, event }: { file: UploadFileInfo, event: ProgressEvent }) {
  let res = (event.target as XMLHttpRequest);
  let data = JSON.parse(res.response);
  edit_info.avatar_mid = data.mid;
  edit_info.avatar_url = data.url;
  window.$message.success("上传成功OvO");
}

function OpenEditInfo() {
  edit_info.avatar_url = user.value.avatar;
  edit_info.nickname = user.value.nickname;
  edit_info.motto = user.value.motto;
  edit_info.model = true;
}

function EditInfo() {
  http.put("/user/info", {
    avatar: edit_info.avatar_mid,
    nickname: edit_info.nickname,
    motto: edit_info.motto
  }).then(() => {
    edit_info.model = false;
  })
}

</script>

<template>
  <div class="container">
    <n-modal :show="edit_info.model">
      <n-card style="width: 600px" title="编辑信息">
        <n-avatar size="large" round :src="user.avatar + store.img_suffix" />
        <n-upload :action="upload_url" :headers="upload_head" @finish="UploadHandler" :max="1">
          <n-button block>上传头像</n-button>
        </n-upload>

        <p style="margin-bottom: 0;">昵称</p>
        <n-input v-model:value="user.nickname" maxlength="24"></n-input>

        <p style="margin-bottom: 0;">格言/简介</p>
        <n-input v-model:value="user.motto" type="textarea"></n-input>

        <template #footer>
          <n-space>
            <n-button @click="EditInfo" type="success" ghost>提交</n-button>
            <n-button @click="edit_info.model = false" type="error" ghost>取消</n-button>
          </n-space>
        </template>
      </n-card>
    </n-modal>

    <n-card title="你好鸭ヾ(´▽｀))" v-if="user.type">
      <div style="display: flex;align-items: center;">
        <Avatar :user="user" round :size="42" />
        <span style="margin-left: 4px;">
          <div style="font-size: 17px;">{{ user.nickname }}</div>
          <div style="margin-top: -4px;">uid:{{ user.id }}</div>
        </span>
      </div>
      <n-tag round :bordered="false" size="small" :color="{color:user.type.color?user.type.color:'#FF9A57',textColor:'#FFF'}">
        用户类型：{{ user.type.text }}
      </n-tag>
      <n-alert title="格言/简介" type="info" :show-icon="false" style="white-space:pre-wrap;margin-top: 14px;">
        {{ user.motto }}
      </n-alert>
      <p style="color:#abc;font-size:14px;">于 {{ FormatTime(user.create_time) }} 来到BIT101</p>
      <n-button v-if="route.params.id == '0'" @click="OpenEditInfo" block>编辑信息</n-button>
    </n-card>

    <br />
  </div>
</template>