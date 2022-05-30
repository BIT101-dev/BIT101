<!--
 * @Author: flwfdd
 * @Date: 2022-05-28 00:01:07
 * @LastEditTime: 2022-05-30 21:55:30
 * @Description: 
 * _(:з」∠)_
-->
<script setup lang="ts">
import { GlobalThemeOverrides } from 'naive-ui'
import { MenuRound } from '@vicons/material'
import Theme from '@/utils/naive-ui-theme-overrides.json'
import { useRouter, useRoute } from 'vue-router';
import MessageContent from './components/MessageContent.vue';

const themeOverrides: GlobalThemeOverrides = Theme;
const router = useRouter();
const route = useRoute();
</script>

<template>
  <n-config-provider :theme-overrides="themeOverrides">
    <n-message-provider>
      <MessageContent />
    </n-message-provider>
    <n-layout>
      <n-layout-header bordered style="background-color:#FF9A57;">
        <div class="container" style="height:42px;display: flex;align-items: center;padding: 4px;">
          <n-button circle color="#FF9A57" text-color="#FFF" style="font-size: 33px;margin-top:3px;" size="large">
            <n-icon>
              <MenuRound />
            </n-icon>
          </n-button>
          <n-button @click="router.push('/')" text style="font-size: 24px;color:#FFF">BITself</n-button>
        </div>
      </n-layout-header>

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
#app {
  font-family: Noto Serif SC;
  font-style: normal;
  font-weight: 500;
}

.container {
  max-width: 666px;
  margin: auto;
}
</style>
