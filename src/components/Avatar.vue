<!--
 * @Author: flwfdd
 * @Date: 2023-10-17 20:24:22
 * @LastEditTime: 2023-10-30 18:39:55
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import store from '@/utils/store';
import { VerifiedFilled } from '@vicons/material';
import { User } from '@/utils/types';
import { PropType } from 'vue';
import ImageViewer from '@/components/ImageViewer/ImageViewer.vue';

const props = defineProps({
  user: {
    type: Object as PropType<User>,
    required: true
  },
  round: {
    type: Boolean,
    default: false
  },
  size: {
    type: Number,
    default: 42
  },
  preview: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
  <div style="font-size:0;position:relative;">
    <ImageViewer :src="props.user.avatar" lazy object-fit="fill" :preview-disabled="!props.preview" />
    <n-icon v-if="props.user.identity.color" :component="VerifiedFilled" :size="0.42 * props.size"
      :color="props.user.identity.color" style="position:absolute;right:0;bottom:0;" />
  </div>
</template>