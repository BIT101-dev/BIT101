<!--
 * @Author: flwfdd
 * @Date: 2023-03-30 14:26:39
 * @LastEditTime: 2023-03-30 16:29:45
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import router from '@/router';
import http from '@/utils/request';
import { FormatTime } from '@/utils/tools';
import { ThumbUpFilled, TextsmsFilled } from '@vicons/material';
import { onMounted, reactive, ref } from 'vue';

const messages = reactive({
    obj: "",
    last_id: 0,
    end: false,
    loading: false,
    list: [] as any,
})

const unread_likes_num = ref(0);
function LoadLikesNum() {
    http.get("/messages/unread_likes_num").then(res => {
        unread_likes_num.value = res.data.unread_num;
    })
}

const unread_comments_num = ref(0);
function LoadCommentsNum() {
    http.get("/messages/unread_comments_num").then(res => {
        unread_comments_num.value = res.data.unread_num;
    })
}

function LoadMessages() {
    messages.loading = true;
    http.get("/messages", { params: { 'obj': messages.obj, 'last_id': messages.last_id } }).then(res => {
        messages.loading = false;

        if (res.data.length == 0) {
            messages.end = true;
        } else {
            messages.list = messages.list.concat(res.data);
            messages.last_id = messages.list[messages.list.length - 1].id;
        }
    })
}

function LoadLikes() {
    messages.obj = "like";
    messages.last_id = 0;
    messages.end = false;
    messages.list = [];
    unread_likes_num.value = 0;
    LoadMessages();
}

function LoadComments() {
    messages.obj = "comment";
    messages.last_id = 0;
    messages.end = false;
    messages.list = [];
    unread_comments_num.value = 0;
    LoadMessages();
}

onMounted(() => {
    LoadLikesNum();
    LoadCommentsNum();
})

function GetTypeName(type: string) {
    if (type.startsWith("like")) return "赞";
    if (type.startsWith("comment")) return "评论";
}

function GetUrl(obj: string) {
    if (obj.startsWith("paper")) return "/paper/show/" + obj.substring(5);
    if (obj.startsWith("course")) return "/course/show/" + obj.substring(6);
    return "";
}

</script>

<template>
    <div class="container">
        <n-card title="消息 | Message">
            <n-space>
                <n-badge :value="unread_likes_num" :max="99">
                    <n-button @click="LoadLikes">
                        <template #icon>
                            <n-icon color="#fb7299">
                                <ThumbUpFilled />
                            </n-icon>
                        </template>
                        收到的赞
                    </n-button>
                </n-badge>

                <n-badge :value="unread_comments_num" :max="99">
                    <n-button @click="LoadComments">
                        <template #icon>
                            <n-icon color="#fb7299">
                                <TextsmsFilled />
                            </n-icon>
                        </template>
                        收到的评论
                    </n-button>
                </n-badge>
            </n-space>

        </n-card>

        <n-divider></n-divider>

        <template v-if="messages.obj">
            <n-card v-for="i in messages.list" hoverable style="margin-bottom:11px;background-color: #F0FCFF;">
                <n-ellipsis :line-clamp="2" :tooltip="false" style="font-size:15px;">
                    <a v-if="i['from_user']['id'] != 0" :href="'/#/user/' + i['from_user']['id']" target="_blank"
                        style="text-decoration:none;color:#FF8533">
                        @{{ i['from_user']['nickname'] }}
                    </a>
                    {{ GetTypeName(i['obj']) }}了你的{{ GetTypeName(i['type']) }} {{ i['content'] }}
                </n-ellipsis>
                <n-space style="color:#809BA8;font-size:14px;">
                    {{ FormatTime(i['update_time']) }}
                    <n-button @click="router.push(GetUrl(i['link_obj']))" text>查看></n-button>
                </n-space>
            </n-card>
            <n-divider style="color:#809BA8;font-size:14px;">已加载{{ messages.list.length }}条</n-divider>
            <n-button block @click="LoadMessages()" :disabled="messages.end" :loading="messages.loading">
                {{ messages.end ? '木有更多了' : '加载更多' }}</n-button>
        </template>

    </div>
</template>