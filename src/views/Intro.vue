<!--
 * @Author: flwfdd
 * @Date: 2023-10-30 11:12:16
 * @LastEditTime: 2024-02-26 17:09:00
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import store from '@/utils/store';
import { useRouter } from 'vue-router';

const router=useRouter();

if (store.fake_cookie) {
  router.replace('/gallery');
} else {
  router.replace('/home');
}

</script>

<template>
</template>