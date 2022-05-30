<!--
 * @Author: flwfdd
 * @Date: 2022-05-29 17:40:17
 * @LastEditTime: 2022-05-29 19:23:56
 * @Description: 规避Vue的Inject限制，给全局提供Message
 * _(:з」∠)_
-->
<script setup lang="ts">
import { useMessage } from 'naive-ui';

window.$message=useMessage();
</script>

<template></template>