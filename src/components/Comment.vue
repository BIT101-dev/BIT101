<!--
 * @Author: flwfdd
 * @Date: 2022-07-17 01:40:53
 * @LastEditTime: 2022-07-27 23:50:06
 * @Description: 评论模块
 * _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import { onMounted, reactive, ref } from 'vue';
import { MessageOutlined } from '@vicons/material';
import store from '@/utils/store';
import { FormatTime } from '@/utils/tools';
import { ThumbUpOutlined, ThumbUpFilled, DeleteOutlined, ReplyOutlined } from '@vicons/material';


const props = defineProps(['obj'])

const now_comment = reactive({
  text: '',
  anonymous: false,
  loading: false,
})

const sub_comment = reactive({
  modal: false,
  parent: {},
  reply_user: {},
})

const comments = reactive({
  order: 'default',
  page: 0,
  end: false,
  list: [] as any,
  loading: false,
})

const sub_comments = reactive({
  modal: false,
  parent: {},
  order: 'old',
  page: 0,
  end: false,
  list: [] as any[],
  loading: false,
})

function Comment(obj: string, parent_list: any, reply_user = '0') {
  now_comment.loading = true;
  http.post("/reaction/comment/", {
    obj: obj,
    text: now_comment.text,
    anonymous: now_comment.anonymous ? '1' : '',
    reply_user: reply_user,
  }).then(res => {
    parent_list.unshift(res.data);
    now_comment.text = "";
    now_comment.anonymous = false;
    now_comment.loading = false;
    sub_comment.modal = false;
  }).catch(() => {
    now_comment.loading = false;
  })
}

function OpenReplyModal(parent: any, reply_user = '0') {
  sub_comment.modal = true;
  sub_comment.parent = parent;
  sub_comment.reply_user = reply_user;
}

function LoadComments(obj: string, cmts: any) {
  cmts.loading = true;
  http.get('/reaction/comments/', {
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


function Like(i: any) {
  i.like_loading = true;
  http.post("/reaction/like/", { 'obj': 'comment' + i.id })
    .then(res => {
      i.like = res.data.like;
      i.like_num = res.data.like_num;
      i.like_loading = false;
    }).catch(() => { i.like_loading = false; })
}

function Delete(i: any, cmts: any) {
  http.delete("/reaction/comment/?id=" + i.id)
    .then(() => {
      cmts.list = cmts.list.filter((x: any) => (x.id != i.id))
    })
}

onMounted(() => {
  LoadComments(props.obj, comments);
})
</script>

<template>
  <n-space vertical>
    <n-input v-model:value="now_comment.text" type="textarea" placeholder="沉默不是金" />
    <n-space justify="space-between">
      <n-button @click="now_comment.anonymous = !now_comment.anonymous" ghost>匿名:{{ now_comment.anonymous ? '是' :
          '否'
      }}</n-button>
      <n-button @click="Comment(props.obj, comments['list'])" type="info" ghost :disabled="now_comment.loading"
        :loading="now_comment.loading" icon-placement="right">
        <template #icon>
          <n-icon>
            <MessageOutlined />
          </n-icon>
        </template>
        发表评价
      </n-button>
    </n-space>
  </n-space>


  <template v-for="i in comments.list">
    <n-divider></n-divider>
    <div style="display: flex;align-items: top;color:#3E5C6B;">
      <div>
        <router-link :to="'/user/' + i['user']['id']">
          <n-avatar :src="i['user']['avatar'] + store.img_suffix" />
        </router-link>
      </div>
      <span style="margin-left: 4px;margin-top:-6px">
        <div style="font-size: 16px;">{{ i['user']['nickname'] }}</div>
        <div style="margin-top: -4px;font-size:14px;">{{ FormatTime(i['create_time']) }}</div>
        <div style="white-space: pre-wrap;margin-top:4px;">{{ i['text'] }}</div>
        <n-space>
          <n-button @click="Like(i)" color="#fb7299" text :loading="i['like_loading']" :disabled="i['like_loading']">
            <template #icon>
              <n-icon>
                <ThumbUpFilled v-if="i['like']" />
                <ThumbUpOutlined v-else />
              </n-icon>
            </template>
            {{ i['like_num'] }}人赞同
          </n-button>

          <n-button @click="OpenReplyModal(i)" text>
            <template #icon>
              <n-icon>
                <ReplyOutlined />
              </n-icon>
            </template>
            回复
          </n-button>

          <n-popconfirm @positive-click="Delete(i, comments)" :show-icon="false" positive-text="确定" negative-text="取消">
            <template #trigger>
              <n-button v-show="i['own']" text>
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
        </n-space>

        <div v-if="i['comment_num'] != 0" style="background-color:#fafafa;padding:4px;border-radius: 4px;">
          <div v-for="j in i.sub.slice(0, 3)" style="margin:4px;">
            {{ j['user']['nickname'] }}：
            <span v-if="j['reply_user']">@{{ j['reply_user']['nickname'] }}</span>
            <span style="white-space: pre-wrap;margin-top:4px;">{{ j['text'] }}</span>
          </div>
          <n-button @click="OpenSubComments(i)" text>共 {{ i['comment_num'] }} 条回复>></n-button>
        </div>
      </span>
    </div>
  </template>
  <n-divider style="color:#809BA8;font-size:14px;">已加载{{ comments.list.length }}条</n-divider>
  <n-button block @click="LoadComments(props.obj, comments)" :disabled="comments.end" :loading="comments.loading">
    {{ comments.end ? '木有更多了' : '加载更多' }}</n-button>

  <n-modal v-model:show="sub_comment.modal" preset="card" style="width:624px"
    :title="'回复' + (sub_comment.reply_user == '0' ? '' : '@' + sub_comment.reply_user['nickname'])">
    <n-space vertical>
      <n-input v-model:value="now_comment.text" type="textarea" placeholder="沉默不是金" />
      <n-space justify="space-between">
        <n-button @click="now_comment.anonymous = !now_comment.anonymous" ghost>匿名:{{ now_comment.anonymous ? '是' :
            '否'
        }}</n-button>
        <n-button
          @click="Comment('comment' + sub_comment.parent['id'], sub_comment.parent['sub'], sub_comment.reply_user['id'])"
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

  <n-modal v-model:show="sub_comments.modal" preset="card" style="width:624px">
    <n-scrollbar style="max-height:624px">
      <div style="display: flex;align-items: top;color:#3E5C6B;">
        <div>
          <router-link :to="'/user/' + sub_comments.parent['user']['id']">
            <n-avatar :src="sub_comments.parent['user']['avatar'] + store.img_suffix" />
          </router-link>
        </div>
        <span style="margin-left: 4px;margin-top:-6px">
          <div style="font-size: 16px;">{{ sub_comments.parent['user']['nickname'] }}</div>
          <div style="margin-top: -4px;font-size:14px;">{{ FormatTime(sub_comments.parent['create_time']) }}</div>
          <div style="white-space: pre-wrap;margin-top:4px;">{{ sub_comments.parent['text'] }}</div>
        </span>
      </div>
      
      <template v-for="i in sub_comments.list">
        <n-divider style="margin:11px"></n-divider>
        <div style="display: flex;align-items: top;color:#3E5C6B;">
          <div>
            <router-link :to="'/user/' + i['user']['id']">
              <n-avatar :src="i['user']['avatar'] + store.img_suffix" />
            </router-link>
          </div>
          <span style="margin-left: 4px;margin-top:-6px">
            <div style="font-size: 16px;">{{ i['user']['nickname'] }}</div>
            <div style="margin-top: -4px;font-size:14px;">{{ FormatTime(i['create_time']) }}</div>
            <div style="white-space: pre-wrap;margin-top:4px;">
              <router-link v-if="i['reply_user']" :to="'/user/' + i['reply_user']['id']" style="text-decoration: none;">
                @{{ i['reply_user']['nickname'] }}</router-link>
                {{ i['text'] }}
            </div>
            <n-space>
              <n-button @click="Like(i)" color="#fb7299" text :loading="i['like_loading']"
                :disabled="i['like_loading']">
                <template #icon>
                  <n-icon>
                    <ThumbUpFilled v-if="i['like']" />
                    <ThumbUpOutlined v-else />
                  </n-icon>
                </template>
                {{ i['like_num'] }}人赞同
              </n-button>

              <n-button @click="OpenReplyModal(sub_comments.parent, i['user'])" text>
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
                  <n-button v-show="i['own']" text>
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
            </n-space>
          </span>
        </div>
      </template>
      <n-divider style="color:#809BA8;font-size:14px;">已加载{{ sub_comments.list.length }}条</n-divider>
      <n-button block @click="LoadComments('comment' + sub_comments.parent['id'], sub_comments)"
        :disabled="sub_comments.end" :loading="sub_comments.loading">
        {{ sub_comments.end ? '木有更多了' : '加载更多' }}</n-button>
    </n-scrollbar>
  </n-modal>

</template>