<!--
 * @Author: flwfdd
 * @Date: 2022-05-28 00:01:07
 * @LastEditTime: 2025-03-19 02:33:48
 * @Description: 
 * _(:з」∠)_
-->
<script setup lang="ts">
import { NIcon, darkTheme, lightTheme, useOsTheme, useThemeVars } from 'naive-ui'
import LightThemeOverrides from '@/utils/naive-ui-light-theme-overrides.json';
import DarkThemeOverrides from '@/utils/naive-ui-dark-theme-overrides.json';
import { useRouter, useRoute } from 'vue-router';
import { h, ref, onMounted, computed } from 'vue';
import MenuRound from '@vicons/material/MenuRound'
import HomeOutlined from '@vicons/material/HomeOutlined'
import FingerprintOutlined from '@vicons/material/FingerprintOutlined'
import PersonOutlined from '@vicons/material/PersonOutlined'
import SchoolOutlined from '@vicons/material/SchoolOutlined'
import ArticleOutlined from '@vicons/material/ArticleOutlined'
import RefreshOutlined from '@vicons/material/RefreshOutlined'
import BookOutlined from '@vicons/material/BookOutlined'
import ArrowBackOutlined from '@vicons/material/ArrowBackOutlined'
import CalendarMonthOutlined from '@vicons/material/CalendarMonthOutlined'
import MailOutlined from '@vicons/material/MailOutlined'
import MapOutlined from '@vicons/material/MapOutlined'
import ForumOutlined from '@vicons/material/ForumOutlined'
import BrightnessAutoOutlined from '@vicons/material/BrightnessAutoOutlined'
import LightModeOutlined from '@vicons/material/LightModeOutlined'
import DarkModeOutlined from '@vicons/material/DarkModeOutlined'
import QuestionCircleOutlined from "@vicons/antd/QuestionCircleOutlined"
import BookmarkBorderOutlined from "@vicons/material/BookmarkBorderOutlined"
import GlobalComponents from './components/GlobalComponents.vue';
import { hitokoto, WatchNetwork } from './utils/tools';
import http from './utils/request';
import axios from 'axios';

import store from './utils/store';

const isDark = computed(() => {
  if (store.theme_mode === "auto") {
    return useOsTheme().value === "dark";
  } else {
    return store.theme_mode === "dark";
  }
})
const theme = computed(() => isDark.value ? darkTheme : lightTheme);
const themeOverrides = computed(() => isDark.value ? DarkThemeOverrides : LightThemeOverrides);
const themeVars = useThemeVars();

function ChangeTheme() {
  if (store.theme_mode === "auto") {
    store.theme_mode = "light";
  } else if (store.theme_mode === "light") {
    store.theme_mode = "dark";
  } else {
    store.theme_mode = "auto";
  }
}

const router = useRouter();
const route = useRoute();

const drawer_model = ref(false);

function renderIcon(icon: any) {
  return () => h(NIcon, null, { default: () => h(icon) })
}
const menu_options = computed(() => {
  const home = {
    label: "回家",
    key: '/home/',
    icon: renderIcon(HomeOutlined)
  }
  const login = {
    label: "登录",
    key: '/login/',
    icon: renderIcon(FingerprintOutlined)
  }
  const my = {
    label: "我的",
    key: '/user/0/',
    icon: renderIcon(PersonOutlined)
  }
  const gallery = {
    label: "话廊",
    key: '/gallery/',
    icon: renderIcon(ForumOutlined)
  }
  const paper = {
    label: "文章",
    key: '/paper/',
    icon: renderIcon(ArticleOutlined)
  }
  const course = {
    label: "课程",
    key: '/course/',
    icon: renderIcon(BookOutlined)
  }
  const subscription = {
    label: "订阅",
    key: '/subscription/',
    icon: renderIcon(BookmarkBorderOutlined)
  }
  const score = {
    label: "成绩",
    key: '/score/',
    icon: renderIcon(SchoolOutlined)
  }
  const schedule = {
    label: "课表",
    key: '/schedule/',
    icon: renderIcon(CalendarMonthOutlined)
  }
  const map = {
    label: "地图",
    key: '/map/',
    icon: renderIcon(MapOutlined)
  }
  const about = {
    label: "关于",
    key: '/about/',
    icon: renderIcon(QuestionCircleOutlined)
  }

  if (store.fake_cookie)
    return [home, login, my, gallery, paper, course, subscription, score, schedule, map, about];
  return [home, login, my, about];
});

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
  // 自动升级到https
  if (location.protocol == 'http:') {
    axios.get(`https${location.href.substring(4)}`).then(() => {
      location.protocol = 'https:';
    })
  };

  // 监测网络
  WatchNetwork();

  LoadUnreadNum();
})

</script>

<template>
  <n-config-provider :theme-overrides="themeOverrides" :theme="theme">
    <n-global-style />
    <n-el>
      <GlobalComponents></GlobalComponents>
      <n-layout>
        <n-layout-header bordered style="background-color:var(--primary-color)">
          <n-space class="container" justify="space-between">
            <div style="height:42px;display: flex;align-items: center;padding: 4px;">
              <n-button @click="drawer_model = true" circle type="primary" text-color="#FFF"
                style="font-size: 33px;margin-top:3px;" size="large">
                <n-icon>
                  <MenuRound />
                </n-icon>
              </n-button>
              <n-button @click="router.push('/home')" text style="font-size: 24px;color:#FFF">BIT101</n-button>
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
              <n-button @click="ChangeTheme" quaternary circle size="large" color="white">
                <template #icon>
                  <n-icon>
                    <LightModeOutlined v-if="store.theme_mode == 'light'" />
                    <DarkModeOutlined v-else-if="store.theme_mode == 'dark'" />
                    <BrightnessAutoOutlined v-else />
                  </n-icon>
                </template>
              </n-button>
              <n-button @click="unread_num = 0, router.push('/message/')" quaternary circle size="large" color="white"
                style="margin-right:4px">
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
            <keep-alive :max="42">
              <component :is="Component" v-if="route.meta.keepAlive != false" :key="route.fullPath" />
            </keep-alive>
            <component :is="Component" v-if="route.meta.keepAlive == false" />
          </router-view>
        </n-layout-content>


        <n-layout-footer style="text-align:center;min-height: 11vh;">
          <h4 style="margin: auto;font-size: 14px;">{{ hitokoto }}</h4>
          <div><n-button @click="ToTop" text size="large">👆回到顶部👆</n-button></div>
          <div>
            <n-a href="https://github.com/BIT101-dev" target="_blank">GitHub</n-a>
            ｜
            <n-a href="https://bit101-project.feishu.cn/wiki/OY1Xw6y27iNZqgkSDCkc5Cfdnjc" target="_blank">加入BIT101</n-a>
          </div>
          <div style="font-size: 14px;">Powered⚡ by BIT101 Project Team with 💖.</div>

        </n-layout-footer>
      </n-layout>
    </n-el>
  </n-config-provider>
</template>

<style>
@font-face {
  font-family: "Noto Serif";
  src: local("Noto Serif SC Light"),
    local("Noto Serif SC"),
    local("Noto Serif CJK Light"),
    local("Noto Serif CJK"),
    local("Source Han Serif CN Light"),
    local("Source Han Serif CN");
  font-display: swap;
  font-weight: 300;
}

@font-face {
  font-family: "Noto Serif";
  src: local("Noto Serif SC Medium"),
    local("Noto Serif SC"),
    local("Noto Serif CJK Medium"),
    local("Noto Serif CJK"),
    local("Source Han Serif CN Medium"),
    local("Source Han Serif CN");
  font-display: swap;
  font-weight: 500;
}

@font-face {
  font-family: "Noto Serif";
  src: local("Noto Serif SC Bold"),
    local("Noto Serif CJK Bold"),
    local("Source Han Serif CN Bold");
  font-display: swap;
  font-weight: 700;
}

@font-face {
  font-family: "Noto Serif";
  src: local("Noto Serif SC Heavy"),
    local("Noto Serif CJK Heavy"),
    local("Source Han Serif CN Heavy");
  font-display: swap;
  font-weight: 800;
}

#app,
body {
  font-family: "Noto Serif", "Noto Serif SC", serif;
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
