<!--
 * @Author: flwfdd
 * @Date: 2022-06-01 14:21:01
 * @LastEditTime: 2022-07-10 19:26:41
 * @Description: 用户中心
 * _(:з」∠)_
-->
<script setup lang="ts">
import { FormatTime, hitokoto } from '@/utils/tools';
import http from '@/utils/request';
import { onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';
import store from '@/utils/store';
import { UploadFileInfo } from 'naive-ui';


const user = reactive({
    id: "",
    sid: "",
    nickname: "",
    avatar: "",
    motto: "",
    register_time: ""
});
function GetInfo(uid: any) {
    http.get("/user/info/?id=" + uid)
        .then(res => {
            user.id = res.data.id;
            user.sid = res.data.sid;
            user.nickname = res.data.nickname;
            user.avatar = res.data.avatar;
            user.motto = res.data.motto;
            user.register_time = FormatTime(res.data.register_time);
        })
}

const route = useRoute();
onMounted(() => {
    GetInfo(route.params.id);
})

const edit_model = ref(false);
const upload_url = store.api_url + "/upload/image/";
const upload_head = {
    'fake-cookie': store.fake_cookie
}

function UploadHandler({file,event}:{file:UploadFileInfo,event:ProgressEvent}){
    let res=(event.target as XMLHttpRequest);
    let data=JSON.parse(res.response);
    user.avatar=data.url;
    window.$message.success("上传成功OvO");
}

function EditInfo(){
    http.post("/user/info/",{
        avatar:user.avatar,
        nickname:user.nickname,
        motto:user.motto
    }).then(()=>{
        edit_model.value=false;
    })
}

</script>

<template>
    <div class="container">
        <n-modal :show="edit_model">
            <n-card style="width: 600px" title="编辑信息">
                <n-avatar size="large" round :src="user.avatar" />
                <n-upload :action="upload_url" :headers="upload_head" @finish="UploadHandler" :max="1">
                    <n-button block>上传头像</n-button>
                </n-upload>

                <p style="margin-bottom: 0;">昵称</p>
                <n-input v-model:value="user.nickname"></n-input>

                <p style="margin-bottom: 0;">格言/简介</p>
                <n-input v-model:value="user.motto" type="textarea"></n-input>

                <template #footer>
                    <n-space>
                        <n-button @click="EditInfo" type="success" ghost>提交</n-button>
                        <n-button @click="edit_model = false" type="error" ghost >取消</n-button>
                    </n-space>
                </template>
            </n-card>
        </n-modal>

        <n-card title="你好鸭ヾ(´▽｀))">
            <div style="display: flex;align-items: center;">
                <n-avatar size="large" round :src="user.avatar" />
                <span style="margin-left: 4px;">
                    <div style="font-size: 17px;">{{ user.nickname }}</div>
                    <div style="margin-top: -4px;">uid:{{ user.id }}</div>
                </span>
            </div>
            <br />
            <n-alert title="格言/简介" type="info" :show-icon="false" style="white-space: pre-wrap;" >
                {{ user.motto}}
            </n-alert>
            <p style="color: #abc;">于 {{ user.register_time }} 来到BITself</p>
            <n-button v-if="route.params.id == '0'" @click="edit_model = true" block>编辑信息</n-button>
        </n-card>

        <br />
    </div>
</template>