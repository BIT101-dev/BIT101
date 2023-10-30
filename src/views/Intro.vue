<!--
 * @Author: flwfdd
 * @Date: 2023-10-30 11:12:16
 * @LastEditTime: 2023-10-30 11:15:40
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import store from '@/utils/store';
import { OpenLink } from '@/utils/tools';


if (store.fake_cookie) {
  OpenLink('/gallery');
} else {
  OpenLink('/home');
}

</script>

<template>
</template>