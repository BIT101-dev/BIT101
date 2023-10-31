<!--
 * @Author: flwfdd
 * @Date: 2023-10-20 17:39:36
 * @LastEditTime: 2023-10-31 10:40:37
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import { onActivated, onDeactivated, onMounted, onUnmounted, ref, watch } from 'vue';
import { onBeforeRouteLeave, onBeforeRouteUpdate, useRoute, useRouter } from 'vue-router';
import { FormatTime, Clip, setTitle, OpenLink, Share } from '@/utils/tools';
import { AddCommentOutlined, EditOutlined, ThumbUpOutlined, ThumbUpFilled, ShareOutlined, ErrorOutlined, DeleteOutlined, FeedbackOutlined } from '@vicons/material';
import Comment from '@/components/Comment.vue';
import { Poster } from '@/utils/types';
import Avatar from '@/components/Avatar.vue';
import RenderLink from '@/components/RenderLink.vue';

//Poster数据
const poster = ref({} as Poster)
const actions = ref<HTMLDivElement>()

//加载Poster
function LoadPoster() {
  http.get("/posters/" + poster.value.id)
    .then(res => {
      poster.value = res.data;
      // 设置页面标题
      setTitle(poster.value.title, '话廊')
    })
}

// 点赞
const like_loading = ref(false);
function Like() {
  like_loading.value = true;
  http.post("/reaction/like", { 'obj': 'poster' + poster.value.id })
    .then(res => {
      poster.value.like = res.data.like;
      poster.value.like_num = res.data.like_num;
      like_loading.value = false;
    }).catch(() => { like_loading.value = false; })
}

// 上报
function Stay() {
  http.post("/reaction/stay", { obj: 'poster' + poster.value.id, time: 5 })
}

function SharePoster() {
  let title = 'BIT101话廊｜' + poster.value.title;
  Share(title, title, window.location.href)
}

// 删除
function DeletePoster() {
  http.delete("/posters/" + poster.value.id).then(() => {
    router.go(-1);
  })
}

// 滚动到actions
function ScrollToActions() {
  console.log(actions)
  actions.value!.scrollIntoView({
    behavior: "smooth"
  })
}

const router = useRouter();
const route = useRoute();
let timer = null as any;
onMounted(async () => {
  poster.value.id = Number(route.params.id);
  await LoadPoster();

  // 反馈停留
  timer = setTimeout(() => {
    Stay();
  }, 5000);
})

// 离开页面时清除反馈定时器
onDeactivated(() => {
  timer && clearTimeout(timer);
})

// 编辑后刷新
const path = ref(route.path);
router.afterEach(async (to, from) => {
  if (to.path != path.value) return;
  if (from.name == "gallery_edit" && Number(from.params.id) == poster.value.id) {
    await LoadPoster();
    setTitle(poster.value.title, '话廊')
  }
})

</script>

<template>
  <div class="container" v-if="poster.user">
    <h2 style="color:#00BCD4;margin-top:0px;margin-bottom:11px;word-wrap:break-word;">{{ poster.title }}</h2>

    <div style="display:flex;align-items:center;color:#3E5C6B;margin-bottom:11px;">
      <div @click="OpenLink('/user/' + poster.user.id)" @click.stop="" style="cursor:pointer;">
        <Avatar :user="poster.user" :size="36" round />
      </div>
      <span style="margin-left:4px;">
        <div style="font-size: 16px;">{{ poster.user.nickname }}</div>
        <div style="margin-top: -4px;font-size:14px;">{{ poster.user.identity.text }}</div>
      </span>
    </div>

    <n-space v-if="poster.claim.id != 0 || poster.public == false" style="margin-bottom:11px;">
      <n-tag v-if="poster.public == false" round :bordered="false" type="warning" size="small">
        仅自己可见
        <template #icon>
          <n-icon :component="ErrorOutlined" />
        </template>
      </n-tag>
      <n-tag v-if="poster.claim.id != 0" round :bordered="false" type="error" size="small">
        {{ poster.claim.text }}
        <template #icon>
          <n-icon :component="ErrorOutlined" />
        </template>
      </n-tag>
    </n-space>

    <n-image-group v-if="poster.images.length" show-toolbar-tooltip>
      <n-grid x-gap="5" y-gap="5" :cols="3" style="max-width: 424px;margin-bottom: 11px;">
        <n-gi v-for="image in poster.images">
          <div @click.stop="" style="height:0;padding-bottom:100%;position:relative;">
            <n-image object-fit="cover" :preview-src="image.low_url" :src="image.low_url"
              style="width:100%;height:100%;position:absolute;top:0;left:0;border-radius: 5%;"
              :img-props="{ 'style': 'width:100%;' }" />
          </div>
        </n-gi>
      </n-grid>
    </n-image-group>

    <p v-for="i in poster.text.split('\n')" style="color:#3E5C6B;margin-top:0;word-wrap:break-word;">
      <RenderLink :value="i" />
    </p>

    <n-space>
      <n-tag v-for="i in poster.tags" :bordered="false" round :color="{ color: '#E3F9FF', textColor: '#FF7E29' }">{{ i
      }}</n-tag>
    </n-space>

    <p style="color:#809BA8;font-size:14px;">
      首次发布于 {{ FormatTime(poster.create_time) }}
      <br />
      最后编辑于 {{ FormatTime(poster.edit_time) }}
    </p>

    <!-- 套一个div 让ref类型是HTMLDivElement 方便用ScrollIntoView() -->
    <div ref="actions">
      <n-space style="margin-top:4px" justify="end">
        <n-button v-if="poster.own" @click="OpenLink('/gallery/edit/' + poster.id)" icon-placement="right" ghost>
          <template #icon>
            <n-icon :component="EditOutlined" />
          </template>
          编辑
        </n-button>

        <n-popconfirm v-if="poster.own" @positive-click="DeletePoster" :show-icon="false" positive-text="确定"
          negative-text="取消">
          <template #trigger>
            <n-button icon-placement="right" ghost>
              <template #icon>
                <n-icon :component="DeleteOutlined" />
              </template>
              删除
            </n-button>
          </template>
          汝真断舍离耶？
        </n-popconfirm>

        <n-button @click="router.push('/report/poster' + poster.id)" icon-placement="right" ghost>
          <template #icon>
            <n-icon :component="FeedbackOutlined" />
          </template>
          举报
        </n-button>

        <n-button @click="SharePoster" icon-placement="right" ghost>
          <template #icon>
            <n-icon :component="ShareOutlined" />
          </template>
          分享
        </n-button>

        <n-button @click="Like" icon-placement="right" color="#fb7299" :ghost="!poster.like" :loading="like_loading"
          :disabled="like_loading">
          <template #icon>
            <n-icon :component="poster.like ? ThumbUpFilled : ThumbUpOutlined" />
          </template>
          {{ poster.like_num }}赞同
        </n-button>

      </n-space>
    </div>
    <n-divider style="color:#809BA8;font-size:14px;">现有{{ poster.comment_num }}条评论</n-divider>
    <Comment :obj='"poster" + poster.id'></Comment>
    <n-space vertical style="position:fixed;right:4.2vw;bottom:4.2vw;">
      <n-button @click="ScrollToActions()" circle :bordered="false"
        style="background-color:#FFFA;width:50px;height: 50px;box-shadow: 0 0 11px #ccc;">
        <template #icon>
          <n-icon :component="AddCommentOutlined" size="24" />
        </template>
      </n-button>
    </n-space>
  </div>
</template>