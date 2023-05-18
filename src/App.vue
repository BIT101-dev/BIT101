<!--
 * @Author: flwfdd
 * @Date: 2022-05-28 00:01:07
 * @LastEditTime: 2023-05-18 11:34:22
 * @Description: 
 * _(:з」∠)_
-->
<script setup lang="ts">
import { GlobalThemeOverrides, NIcon } from 'naive-ui'
import Theme from '@/utils/naive-ui-theme-overrides.json'
import { useRouter, useRoute } from 'vue-router';
import { h, ref, onMounted } from 'vue';
import { MenuRound, HomeOutlined, FingerprintOutlined, PersonOutlined, SchoolOutlined, ArticleOutlined, RefreshOutlined, BookOutlined, ArrowBackOutlined, CalendarMonthOutlined, MailOutlined, MapOutlined } from '@vicons/material';
import { QuestionCircleOutlined } from "@vicons/antd"
import GlobalComponents from './components/GlobalComponents.vue';
import { hitokoto } from './utils/tools';
import http from './utils/request';

const themeOverrides: GlobalThemeOverrides = Theme;
const router = useRouter();
const route = useRoute();

const drawer_model = ref(false);

function renderIcon(icon: any) {
  return () => h(NIcon, null, { default: () => h(icon) })
}
const menu_options = [
  {
    label: "回家",
    key: '/',
    icon: renderIcon(HomeOutlined)
  },
  {
    label: "登录",
    key: '/login/',
    icon: renderIcon(FingerprintOutlined)
  },
  {
    label: "我的",
    key: '/user/0/',
    icon: renderIcon(PersonOutlined)
  },
  {
    label: "文章",
    key: '/paper/',
    icon: renderIcon(ArticleOutlined)
  },
  {
    label: "课程",
    key: '/course/',
    icon: renderIcon(BookOutlined)
  },
  {
    label: "成绩",
    key: '/score/',
    icon: renderIcon(SchoolOutlined)
  },
  {
    label: "课表",
    key: '/schedule/',
    icon: renderIcon(CalendarMonthOutlined)
  },
  {
    label: "地图",
    key: '/map/',
    icon: renderIcon(MapOutlined)
  },
  {
    label: "关于",
    key: '/about/',
    icon: renderIcon(QuestionCircleOutlined)
  }
]
function MenuHandler(key: string) {
  drawer_model.value = false;
  router.push(key);
}

function ToTop() {
  window.scrollTo(0, 0);
}

function Refresh() {
  window.location.reload();
}

const unread_num = ref(0);
function LoadUnreadNum() {
  http.get("/messages/unread_num").then(res => {
    unread_num.value = res.data.unread_num;
  })
}

onMounted(() => {
  LoadUnreadNum();
})

</script>

<template>
  <n-config-provider :theme-overrides="themeOverrides">
    <GlobalComponents></GlobalComponents>
    <n-layout>
      <n-layout-header bordered style="background-color:#FF9A57;">
        <n-space class="container" justify="space-between">
          <div style="height:42px;display: flex;align-items: center;padding: 4px;">
            <n-button @click="drawer_model = true" circle color="#FF9A57" text-color="#FFF"
              style="font-size: 33px;margin-top:3px;" size="large">
              <n-icon>
                <MenuRound />
              </n-icon>
            </n-button>
            <n-button @click="router.push('/')" text style="font-size: 24px;color:#FFF">BIT101</n-button>
          </div>
          <div style="display:flex;align-items:center;height:100%;">
            <n-button @click="router.go(-1)" quaternary circle size="large" color="white">
              <template #icon>
                <n-icon>
                  <ArrowBackOutlined />
                </n-icon>
              </template>
            </n-button>
            <n-button @click="Refresh" quaternary circle size="large" color="white">
              <template #icon>
                <n-icon>
                  <RefreshOutlined />
                </n-icon>
              </template>
            </n-button>
            <n-button @click="unread_num=0,router.push('/message/')" quaternary circle size="large" color="white">
              <template #icon>
                <n-badge :value="unread_num" :max="99">
                  <n-icon color="white">
                    <MailOutlined />
                  </n-icon>
                </n-badge>
              </template>
            </n-button>
          </div>
        </n-space>
      </n-layout-header>

      <n-drawer v-model:show="drawer_model" placement="left" :width="224">
        <n-drawer-content title="BIT101" body-content-style="padding: 4px;">
          <n-menu :options="menu_options" @update:value="MenuHandler" :indent="24"></n-menu>
        </n-drawer-content>
      </n-drawer>

      <n-layout-content justify="center" style="margin: 11px;min-height: 89vh;">
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" v-if="route.meta.keepAlive != false" :key="route.fullPath" />
          </keep-alive>
          <component :is="Component" v-if="route.meta.keepAlive == false" />
        </router-view>
      </n-layout-content>


      <n-layout-footer style="text-align:center;min-height: 11vh;">
        <h4 style="color: #607d8b;margin: auto;font-size: 14px;">{{ hitokoto }}</h4>
        <div><n-button @click="ToTop" text size="large">👆回到顶部👆</n-button></div>
        <div><n-a href="https://github.com/flwfdd/BIT101" target="_blank">GitHub</n-a></div>
        <div style="font-size: 14px;">Powered⚡ by fdd with 💖.</div>
        
      </n-layout-footer>
    </n-layout>
  </n-config-provider>
</template>

<style>
#app,
body {
  font-family: Noto Serif SC;
  font-style: normal;
  font-weight: 500;
  font-size: 16px;
}

.container {
  max-width: 666px;
  margin: auto;
}

::selection {
  color: #fff;
  background: #00bcd4;
}
</style>
