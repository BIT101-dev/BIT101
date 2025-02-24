<!--
 * @Author: flwfdd
 * @Date: 2023-10-20 17:39:36
 * @LastEditTime: 2024-02-26 16:37:13
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import { onActivated, onDeactivated, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { FormatTime, setTitle, OpenLink, Share, opacityColor } from '@/utils/tools';
import MessageOutlined from '@vicons/material/MessageOutlined'
import EditOutlined from '@vicons/material/EditOutlined'
import ThumbUpOutlined from '@vicons/material/ThumbUpOutlined'
import ThumbUpFilled from '@vicons/material/ThumbUpFilled'
import ShareOutlined from '@vicons/material/ShareOutlined'
import ErrorOutlined from '@vicons/material/ErrorOutlined'
import DeleteOutlined from '@vicons/material/DeleteOutlined'
import FeedbackOutlined from '@vicons/material/FeedbackOutlined'
import Comment from '@/components/Comment.vue';
import { Poster } from '@/utils/types';
import Avatar from '@/components/Avatar.vue';
import RenderLink from '@/components/RenderLink.vue';
import { Md5 } from 'ts-md5';
import ImageViewer from '@/components/ImageViewer/ImageViewer.vue';
import { useThemeVars } from 'naive-ui';

const themeVars = useThemeVars();

//Poster数据
const poster = ref({} as Poster)
const actions = ref<HTMLDivElement>()

//加载Poster
function LoadPoster() {
  return http.get("/posters/" + poster.value.id)
    .then(res => {
      poster.value = res.data;
      // 设置页面标题
      setTitle(poster.value.title, '话廊')
    })
}

// 解析文字
function ParseText(text: string) {
  let l = [];
  let s = "";
  for (let i = 0; i < text.length; i++) {
    if (text[i] == '\n') {
      l.push(s);
      s = "";
    } else {
      s += text[i];
    }
  }
  if (s.length) l.push(s);
  return l;
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

// 分享
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
  actions.value!.scrollIntoView({
    behavior: "smooth",
    block: "center"
  })
}

const router = useRouter();
const route = useRoute();
let timer = null as any;
onMounted(() => {
  poster.value.id = Number(route.params.id);
  LoadPoster();
})

onActivated(() => {
  // 设置页面标题
  if (poster.value.title) setTitle(poster.value.title, '话廊');

  // 反馈停留
  if (!timer) timer = setTimeout(() => {
    Stay();
  }, 5000);
})

// 离开页面时清除反馈定时器
onDeactivated(() => {
  if (timer) {
    clearTimeout(timer);
    timer = null;
  }
})

// 编辑后刷新
const path = ref(route.path);
router.afterEach(async (to, from) => {
  if (to.path != path.value) return;
  if (from.name == "gallery_edit" && Number(from.params.id) == poster.value.id) {
    LoadPoster();
  }
})

</script>

<template>
  <div class="container" v-if="poster.user">
    <n-h2 style="margin-top:0px;margin-bottom:11px;word-wrap:break-word;">{{ poster.title }}</n-h2>

    <div style="display:flex;align-items:center;margin-bottom:11px;">
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

    <ImageViewer v-if="poster.images.length" :images="poster.images" :shrink="false" />

    <div v-for="i in ParseText(poster.text)" :key="Md5.hashStr(i)" style="margin-bottom:4px;">
      <br v-if="i == ''" />
      <div v-else style="margin-top:0;word-wrap:break-word;white-space:pre-wrap;">
        <RenderLink :value="i" />
      </div>
    </div>
    <div style="height:11px;"></div>

    <n-space>
      <n-tag v-for="i in poster.tags" :bordered="false" round
        :color="{ color: opacityColor(themeVars.infoColor, 0.11), textColor: themeVars.primaryColor }">{{ i
        }}</n-tag>
    </n-space>

    <p style="font-size:14px;opacity: 0.66;">
      首次发布于 {{ FormatTime(poster.create_time) }}
      <br />
      最后编辑于 {{ FormatTime(poster.edit_time) }}
    </p>

    <!-- 套一个div 让ref类型是HTMLDivElement 方便用ScrollIntoView() -->
    <div ref="actions" style="display: flex; justify-content: space-between;">
      <n-space style="margin-top:4px">
        <n-button v-if="poster.own" @click="OpenLink('/gallery/edit/' + poster.id)" icon-placement="right" ghost>
          <template #icon>
            <n-icon :component="EditOutlined" />
          </template>
          编辑
        </n-button>

        <n-popconfirm v-if="poster.own" @positive-click="DeletePoster" :show-icon="false" positive-text="确定"
          negative-text="取消">
          <template #trigger>
            <n-button icon-placement="right" ghost type="error">
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
      </n-space>
      <n-space style="margin-top:4px">
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
    <n-divider style="font-size:14px;">现有{{ poster.comment_num }}条评论</n-divider>
    <Comment :obj='"poster" + poster.id'></Comment>

    <n-space vertical style="position:fixed;right:4.2vw;bottom:4.2vw;">
      <n-button @click="ScrollToActions()" circle :bordered="false"
        :style="{ 'background-color': opacityColor(themeVars.baseColor, 0.84), 'width': '50px', 'height': '50px', 'box-shadow': '0 0 11px #CCCCCCCC' }">
        <template #icon>
          <n-icon :component="MessageOutlined" size="24" />
        </template>
      </n-button>
    </n-space>

  </div>
</template>