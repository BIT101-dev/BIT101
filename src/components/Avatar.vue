<!--
 * @Author: flwfdd
 * @Date: 2023-10-17 20:24:22
 * @LastEditTime: 2023-10-18 01:59:16
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import store from '@/utils/store';
import { VerifiedFilled } from '@vicons/material';
import { User } from '@/utils/types';

const props = withDefaults(defineProps<{
    user: User,
    round: boolean,
    size: number
}>(), {
    round: false,
    size: 42
})
</script>

<template>
    <div style="font-size:0;position:relative;">
        <n-avatar :round="props.round" :size="props.size" :src="props.user.avatar + store.img_suffix" />
        <n-icon v-if="props.user.type.color" :component="VerifiedFilled" :size="0.42*props.size" :color="props.user.type.color"
            style="position:absolute;right:0;bottom:0;" />
    </div>
</template>