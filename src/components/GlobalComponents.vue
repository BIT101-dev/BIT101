<!--
 * @Author: flwfdd
 * @Date: 2022-06-26 17:48:33
 * @LastEditTime: 2022-07-17 13:35:07
 * @Description: 所有页面公用的全局组件
 * _(:з」∠)_
-->
<script setup lang="ts">
import MessageContent from './MessageContent.vue';
import {webvpn,WebvpnVerify2} from '@/utils/tools'

</script>

<template>
  <n-message-provider>
    <MessageContent />
  </n-message-provider>
  <n-modal v-model:show="webvpn.model" :mask-closable="false">
    <n-card title="人 工 智 能 识 别" style="width: 224px;text-align: center;">
      <p style="margin-top:0px;">越人工 越智能</p>
      <n-image :src="webvpn.data.captcha" />
      <n-input v-model:value="webvpn.data.captcha_text" placeholder="不会看不出来吧"></n-input>
      <template #footer>
        <n-button @click="WebvpnVerify2" :disabled="!webvpn.data.captcha_text">确认</n-button>
      </template>
    </n-card>
  </n-modal>
</template>