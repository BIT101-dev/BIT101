<!--
 * @Author: flwfdd
 * @Date: 2023-10-29 14:50:59
 * @LastEditTime: 2023-10-29 15:06:09
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import { OpenLink } from '@/utils/tools';
</script>

<template>
  <n-result status="404" title="404 Not Found" description="当万木俱焚 别走近我" size="large" style="margin-top:11vh;">
    <template #footer>
      <n-button @click="OpenLink('/')">溯洄</n-button>
    </template>
  </n-result>
</template>