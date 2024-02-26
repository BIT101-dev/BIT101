<!--
 * @Author: flwfdd
 * @Date: 2023-03-30 14:26:39
 * @LastEditTime: 2024-02-26 17:15:41
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import router from '@/router';
import http from '@/utils/request';
import { FormatTime } from '@/utils/tools';
import { User } from '@/utils/types';
import { ThumbUpFilled, TextsmsFilled, PersonAddFilled, NotificationsFilled } from '@vicons/material';
import { NA } from 'naive-ui';
import { PropType, defineComponent, h, onActivated, onDeactivated, reactive, ref } from 'vue';

interface Message {
  id: number;
  obj: string;
  text: string;
  link_obj: string;
  update_time: string;
  from_user: User;
}

const messages = reactive({
  type: "",
  last_id: 0,
  end: false,
  loading: false,
  list: [] as Message[],
})

const unread_nums = ref({
  like: 0,
  comment: 0,
  follow: 0,
  system: 0,
});
function LoadUnreadNums() {
  http.get("/messages/unread_nums").then(res => {
    unread_nums.value = res.data;
  })
}

function LoadMessages() {
  if (messages.loading || messages.end) return;
  messages.loading = true;
  http.get("/messages", { params: { 'type': messages.type, 'last_id': messages.last_id } }).then(res => {
    messages.loading = false;

    if (res.data.length == 0) {
      messages.end = true;
    } else {
      messages.list = messages.list.concat(res.data);
      messages.last_id = messages.list[messages.list.length - 1].id;
    }
  }).catch(() => { messages.loading = false; })
}

function StartLoadMessages(type: 'like' | 'comment' | 'follow' | 'system') {
  messages.type = type;
  messages.last_id = 0;
  messages.end = false;
  messages.list = [];
  unread_nums.value[type] = 0;
  LoadMessages();
}

function GetObjName(type: string) {
  if (type.startsWith("like")) return "赞";
  if (type.startsWith("poster")) return "帖子";
  if (type.startsWith("comment")) return "评论";
  return "";
}

function GetUrl(obj: string) {
  if (obj.startsWith("paper")) return "/paper/" + obj.substring(5);
  if (obj.startsWith("course")) return "/course/" + obj.substring(6);
  if (obj.startsWith("poster")) return "/gallery/" + obj.substring(6);
  return "";
}

const MessageContent = defineComponent({
  props: {
    message: {
      type: Object as PropType<Message>,
      required: true,
    }
  },
  setup(props) {
    return () => {
      let message = props.message;
      let l = [];
      let user_link = message.from_user.id != 0 ? h(NA, { href: "/user/" + props.message.from_user.id, style: { textDecoration: 'none' } }, '@' + props.message.from_user.nickname) : '';
      let obj_name = GetObjName(message.obj);
      if (messages.type == 'like') {
        l.push(user_link, ' 赞了你的 ', obj_name, ' ', message.text);
      } else if (messages.type == 'comment') {
        l.push(user_link, ' 评论了你的 ', obj_name, ' ', message.text);
      } else if (messages.type == 'follow') {
        l.push(user_link, ' 关注了你');
      } else if (messages.type == 'system') {
        if (message.from_user.id) l.push('关联用户：', user_link, ' ');
        if (message.obj) l.push('关联对象：', message.obj, ' ');
        l.push(message.text);
      }
      return l;
    }
  }
})

const modal = reactive({
  show: false,
  message: {} as Message,
})
function OpenModal(message: Message) {
  modal.message = message;
  modal.show = true;
}

onActivated(() => {
  LoadUnreadNums();
})

onDeactivated(() => {
  modal.show = false;
})

</script>

<template>
  <div class="container">
    <n-card title="消息 | Message">
      <n-space>
        <n-badge :value="unread_nums.like" :max="99">
          <n-button @click="StartLoadMessages('like')">
            <template #icon>
              <n-icon color="#FB7299" :component="ThumbUpFilled" />
            </template>
            收到的赞
          </n-button>
        </n-badge>

        <n-badge :value="unread_nums.comment" :max="99">
          <n-button @click="StartLoadMessages('comment')">
            <template #icon>
              <n-icon color="#FB7299" :component="TextsmsFilled" />
            </template>
            收到的评论
          </n-button>
        </n-badge>

        <n-badge :value="unread_nums.follow" :max="99">
          <n-button @click="StartLoadMessages('follow')">
            <template #icon>
              <n-icon color="#FB7299" :component="PersonAddFilled" />
            </template>
            新增粉丝
          </n-button>
        </n-badge>

        <n-badge :value="unread_nums.system" :max="99">
          <n-button @click="StartLoadMessages('system')">
            <template #icon>
              <n-icon color="#FB7299" :component="NotificationsFilled" />
            </template>
            系统通知
          </n-button>
        </n-badge>
      </n-space>
    </n-card>

    <n-divider></n-divider>

    <template v-if="messages.type">
      <n-card v-for="i in messages.list" hoverable style="margin-bottom:11px;background-color: var(--card-bg-color);">
        <n-ellipsis :line-clamp="2" :tooltip="false" style="font-size:15px;">
          <MessageContent :message="i"></MessageContent>
        </n-ellipsis>
        <n-space style="color:var(--text-color-3);font-size:14px;">
          {{ FormatTime(i.update_time) }}
          <n-button @click="OpenModal(i)" text>详情></n-button>
          <n-button v-if="i.link_obj" @click="router.push(GetUrl(i.link_obj))" text>查看></n-button>
        </n-space>
      </n-card>
      <n-divider style="color:var(--text-color-3);font-size:14px;">已加载{{ messages.list.length }}条</n-divider>
      <n-button block @click="LoadMessages()" :disabled="messages.end" :loading="messages.loading">
        {{ messages.end ? '木有更多了' : '加载更多' }}</n-button>
    </template>

    <n-modal v-model:show="modal.show" preset="card" title="消息详情" style="width:600px;">
      <n-scrollbar style="max-height:75vh;">
        <div style="white-space: pre-wrap;">
          <MessageContent :message="modal.message"></MessageContent>
        </div>
      </n-scrollbar>
    </n-modal>
  </div>
</template>