<!--
 * @Author: flwfdd
 * @Date: 2022-06-01 14:21:01
 * @LastEditTime: 2023-10-25 12:23:01
 * @Description: 用户中心
 * _(:з」∠)_
-->
<script setup lang="ts">
import { FormatTime, OpenLink, hitokoto, setTitle } from '@/utils/tools';
import http from '@/utils/request';
import { onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';
import store from '@/utils/store';
import { UploadFileInfo } from 'naive-ui';
import { User } from '@/utils/types';
import Avatar from '@/components/Avatar.vue';
import { PostersStatus } from '@/components/Posters.vue';

interface UserInfo {
  user: User; // 用户
  following: boolean; // 我是否关注
  follower: boolean; // 是否关注我
  following_num: number; // 关注数量
  follower_num: number; // 粉丝数量
  own: boolean; // 是否是自己
}

const user_info = ref({} as UserInfo);
function GetInfo(uid: any) {
  http.get("/user/info/" + uid)
    .then(res => {
      user_info.value = res.data;
      if (user_info.value.user.id) setTitle(user_info.value.user.nickname, "用户");
    })
}

// 编辑信息
const edit_info = reactive({
  modal: false,
  avatar_mid: "",
  avatar_url: "",
  nickname: "",
  motto: ""
})

// 上传头像用
const upload_url = store.api_url + "/upload/image";
const upload_head = {
  'fake-cookie': store.fake_cookie
}

function UploadHandler({ file, event }: { file: UploadFileInfo, event: ProgressEvent }) {
  let res = (event.target as XMLHttpRequest);
  let data = JSON.parse(res.response);
  edit_info.avatar_mid = data.mid;
  edit_info.avatar_url = data.low_url;
  window.$message.success("上传成功OvO");
}

function OpenEditInfo() {
  edit_info.avatar_url = user_info.value.user.avatar.low_url;
  edit_info.nickname = user_info.value.user.nickname;
  edit_info.motto = user_info.value.user.motto;
  edit_info.modal = true;
}

function EditInfo() {
  http.put("/user/info", {
    avatar_mid: edit_info.avatar_mid,
    nickname: edit_info.nickname,
    motto: edit_info.motto
  }).then(() => {
    GetInfo(route.params.id);
    edit_info.modal = false;
  })
}

// 关注和取关操作
const follow_loading = ref(false);
function Follow() {
  if (follow_loading.value) return;
  follow_loading.value = true;
  http.post("/user/follow/" + user_info.value.user.id).then(res => {
    user_info.value.following = res.data.following;
    user_info.value.follower = res.data.follower;
    user_info.value.following_num = res.data.following_num;
    user_info.value.follower_num = res.data.follower_num;
    window.$message.success(res.data.following ? "关注成功OvO" : "取关成功OvO");
    follow_loading.value = false;
  }).catch(() => { follow_loading.value = false; })
}

const follows = reactive({
  type: "",
  title: "",
  modal: false,
  loading: false,
  end: false,
  page: 0,
  list: [] as User[]
});

function GetFollowList() {
  if (follows.loading) return;
  follows.loading = true;
  http.get("/user/" + follows.type, {
    params: {
      page: follows.page
    }
  }).then(res => {
    if (res.data.length == 0) follows.end = true;
    follows.list = follows.list.concat(res.data);
    follows.page++;
    follows.loading = false;
  }).catch(() => { follows.loading = false; })
}

function ShowFollowingList() {
  if (route.params.id != '0') {
    window.$message.error("只能查看自己的关注列表Orz");
    return;
  }
  follows.type = "followings";
  follows.title = "关注列表";
  follows.page = 0;
  follows.list = [];
  follows.end = false;
  GetFollowList();
  follows.modal = true;
}

const follower_list = ref([] as User[]);
function ShowFollowerList() {
  if (route.params.id != '0') {
    window.$message.error("只能查看自己的粉丝列表Orz");
    return;
  }
  follows.type = "followers";
  follows.title = "粉丝列表";
  follows.page = 0;
  follows.list = [];
  follows.end = false;
  GetFollowList();
  follows.modal = true;
}

// 帖子
const posters = ref({
  mode: 'search',
  search: "",
  order: "new",
  uid: -1
} as PostersStatus
);

const route = useRoute();
onMounted(() => {
  GetInfo(route.params.id);
  posters.value.uid = Number(route.params.id);
})

function Switch() {
  if (route.params.id == '0') {
    OpenLink('/#/user/' + user_info.value.user.id);
    posters.value.uid = user_info.value.user.id;
  }
  else {
    OpenLink('/#/user/0');
    posters.value.uid = 0;
  }
}

</script>

<template>
  <div class="container">
    <n-card title="你好鸭ヾ(´▽｀))" v-if="user_info.user">
      <div style="display: flex;justify-content: space-between;align-items: center;">
        <div style="display: flex;align-items: center;">
          <Avatar :user="user_info.user" round :size="42" />
          <span style="margin-left: 4px;">
            <div style="font-size: 17px;">{{ user_info.user.nickname }}</div>
            <div style="margin-top: -4px;">uid:{{ user_info.user.id }}</div>
          </span>
        </div>

        <n-popconfirm v-if="user_info.following" @positive-click="Follow" :show-icon="false" positive-text="确定"
          negative-text="取消">
          <template #trigger>
            <n-button :loading="follow_loading" :disabled="follow_loading">
              {{ user_info.following ? (user_info.follower ? '已互粉' : '已关注') : '关注' }}
            </n-button>
          </template>
          汝真取关耶？
        </n-popconfirm>
        <n-button v-else @click="Follow" :loading="follow_loading" :disabled="follow_loading">
          {{ user_info.following ? (user_info.follower ? '已互粉' : '已关注') : '关注' }}
        </n-button>
      </div>


      <n-space>
        <n-tag round :bordered="false" size="small"
          :color="{ color: user_info.user.type.color ? user_info.user.type.color : '#FF9A57', textColor: '#FFF' }">
          {{ user_info.user.type.text }}
        </n-tag>
        <n-tag @click="ShowFollowingList" round :bordered="false" size="small"
          :color="{ color: '#FF9A57', textColor: '#FFF' }" style="cursor:pointer">
          {{ user_info.following_num }}关注
        </n-tag>
        <n-tag @click="ShowFollowerList" round :bordered="false" size="small"
          :color="{ color: '#FF9A57', textColor: '#FFF' }" style="cursor:pointer">
          {{ user_info.follower_num }}粉丝
        </n-tag>
      </n-space>

      <n-alert title="格言/简介" type="info" :show-icon="false" style="white-space:pre-wrap;margin-top: 14px;">
        {{ user_info.user.motto }}
      </n-alert>
      <p style="color:#abc;font-size:14px;">于 {{ FormatTime(user_info.user.create_time) }} 来到BIT101</p>
      <n-button v-if="route.params.id == '0'" @click="OpenEditInfo" block>编辑信息</n-button>
      <n-button v-if="user_info.own" @click="Switch" block style="margin-top: 8px;">{{
        route.params.id == '0' ? '切换到访客视角' : '切换到个人中心' }}</n-button>
    </n-card>

    <br />

    <Posters v-if="posters.uid != -1" :value="posters" />

    <n-modal :show="edit_info.modal">
      <n-card style="width: 600px" title="编辑信息">
        <n-avatar size="large" round :src="edit_info.avatar_url" />
        <n-upload :action="upload_url" :headers="upload_head" @finish="UploadHandler" :max="1">
          <n-button block>上传头像</n-button>
        </n-upload>

        <p style="margin-bottom: 0;">昵称</p>
        <n-input v-model:value="edit_info.nickname" maxlength="24"></n-input>

        <p style="margin-bottom: 0;">格言/简介</p>
        <n-input v-model:value="edit_info.motto" type="textarea" maxlength="23333" show-count></n-input>

        <template #footer>
          <n-space>
            <n-button @click="EditInfo" type="success" ghost>提交</n-button>
            <n-button @click="edit_info.modal = false" type="error" ghost>取消</n-button>
          </n-space>
        </template>
      </n-card>
    </n-modal>

    <n-modal v-model:show="follows.modal" preset="card" :title="follows.title" style="width:600px;">
      <n-scrollbar style="max-height:75vh">
        <n-space vertical>
          <template v-for="user in follows.list">
            <div style="display:flex;align-items:center;cursor:pointer" @click="OpenLink('/#/user/' + user.id, true)">
              <Avatar :user="user" :size="36" />
              <div style="margin-left: 4px;">
                <div style="font-size: 16px;margin-top:-4px;">{{ user.nickname }}</div>
                <div style="margin-top: -4px;font-size:14px;">uid:{{ user.id }}</div>
              </div>
            </div>
            <n-divider style="margin:0px;"></n-divider>
          </template>
        </n-space>
        <n-divider style="color:#809BA8;font-size:14px;">已加载{{ follows.list.length }}条</n-divider>
        <n-button block @click="GetFollowList" :disabled="follows.end" :loading="follows.loading">
          {{ follows.end ? '木有更多了' : '加载更多' }}</n-button>
      </n-scrollbar>
    </n-modal>
  </div>
</template>