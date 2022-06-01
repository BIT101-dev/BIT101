<!--
 * @Author: flwfdd
 * @Date: 2022-05-28 01:26:29
 * @LastEditTime: 2022-06-01 15:41:25
 * @Description: 主页
 * _(:з」∠)_
-->
<script setup lang="ts">
import {hitokoto} from '@/utils/tools';
</script>

<template>
  <div class="container" style="text-align: center;">
    <h1 style="margin: 0;color:#00BCD4">
      欢迎来到 BITself !!
    </h1>

    <h4 style="color: #607d8b;">{{ hitokoto }}</h4>
  </div>

</template>


