<!--
 * @Author: flwfdd
 * @Date: 2022-06-26 17:48:33
 * @LastEditTime: 2022-07-17 13:35:07
 * @Description: 所有页面公用的全局组件
 * _(:з」∠)_
-->
<script setup lang="ts">
import MessageContent from './MessageContent.vue';
import BitLoginSmsModal from './BitLoginSmsModal.vue';


</script>

<template>
  <n-message-provider>
    <MessageContent />
  </n-message-provider>
  <BitLoginSmsModal />
</template>
