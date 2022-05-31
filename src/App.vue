<!--
 * @Author: flwfdd
 * @Date: 2022-05-28 00:01:07
 * @LastEditTime: 2022-05-31 22:51:18
 * @Description: 
 * _(:з」∠)_
-->
<script setup lang="ts">
import { GlobalThemeOverrides,NIcon } from 'naive-ui'
import { MenuRound } from '@vicons/material'
import Theme from '@/utils/naive-ui-theme-overrides.json'
import { useRouter, useRoute } from 'vue-router';
import MessageContent from './components/MessageContent.vue';
import { h, ref } from 'vue';
import { HomeOutlined,FingerprintOutlined } from '@vicons/material';

const themeOverrides: GlobalThemeOverrides = Theme;
const router = useRouter();
const route = useRoute();

const drawer_model = ref(false);

function renderIcon (icon: any) {
  return () => h(NIcon, null, { default: () => h(icon) })
}
const menu_options=[
  {
    label:"回家",
    key: '/',
    icon: renderIcon(HomeOutlined)
  },
  {
    label:"登录",
    key: '/login',
    icon: renderIcon(FingerprintOutlined)
  },
]
function MenuHandler(key:string){
  drawer_model.value=false;
  router.push(key);
}
</script>

<template>
  <n-config-provider :theme-overrides="themeOverrides">
    <n-message-provider>
      <MessageContent />
    </n-message-provider>
    <n-layout>
      <n-layout-header bordered style="background-color:#FF9A57;">
        <div class="container" style="height:42px;display: flex;align-items: center;padding: 4px;">
          <n-button @click="drawer_model = true" circle color="#FF9A57" text-color="#FFF"
            style="font-size: 33px;margin-top:3px;" size="large">
            <n-icon>
              <MenuRound />
            </n-icon>
          </n-button>
          <n-button @click="router.push('/')" text style="font-size: 24px;color:#FFF">BITself</n-button>
        </div>
      </n-layout-header>

      <n-drawer v-model:show="drawer_model" placement="left" width="224">
        <n-drawer-content title="BITself" body-content-style="padding: 4px;">
          <n-menu :options="menu_options" @update:value="MenuHandler" indent="24"></n-menu>
        </n-drawer-content>
      </n-drawer>

      <n-layout-content justify="center" style="margin: 11px;">
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" v-if="route.meta.keepAlive" :key="route.meta.keepAliveKey" />
          </keep-alive>
          <component :is="Component" v-if="!route.meta.keepAlive" />
        </router-view>
      </n-layout-content>

      <n-layout-footer>
        <div class="container" style="text-align:center">Powered by fdd.</div>
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
}

.container {
  max-width: 666px;
  margin: auto;
}
</style>
