<!--
 * @Author: flwfdd
 * @Date: 2023-10-17 20:24:22
 * @LastEditTime: 2023-10-28 11:50:39
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import store from '@/utils/store';
import { VerifiedFilled } from '@vicons/material';
import { User } from '@/utils/types';
import { PropType } from 'vue';

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
    <n-image :width="props.size" :height="props.size" :src="props.user.avatar.low_url" lazy object-fit="fill"
      :img-props="{ style: props.round ? 'border-radius:50%;' : '' }" :preview-disabled="!props.preview" />
    <n-icon v-if="props.user.type.color" :component="VerifiedFilled" :size="0.42 * props.size"
      :color="props.user.type.color" style="position:absolute;right:0;bottom:0;" />
  </div>
</template>