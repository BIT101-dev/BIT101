<!--
 * @Author: flwfdd
 * @Date: 2023-10-30 11:12:16
 * @LastEditTime: 2024-02-21 21:24:43
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import store from '@/utils/store';
import { OpenLink } from '@/utils/tools';
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