<!--
 * @Author: flwfdd
 * @Date: 2025-03-19 01:10:21
 * @LastEditTime: 2025-03-19 02:20:32
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import http from '@/utils/request';
import { SubscriptionLevel } from '@/utils/types';
import BookmarkFilled from '@vicons/material/BookmarkFilled';
import BookmarkBorderFilled from '@vicons/material/BookmarkBorderFilled';
import { computed, PropType, ref, watch } from 'vue';


const props = defineProps({
    obj: {
        type: String,
        required: true
    },
    level: {
        type: Number,
        required: true
    }
})


const level = ref(props.level);
watch(() => props.level, (v) => {
    level.value = v;
});
const loading = ref(false);

const options = computed(() => [
    {
        key: SubscriptionLevel.None,
        label: '取消订阅',
        disabled: level.value == SubscriptionLevel.None
    },
    {
        key: SubscriptionLevel.Silent,
        label: '悄悄收藏',
        disabled: level.value == SubscriptionLevel.Silent
    },
    {
        key: SubscriptionLevel.Update,
        label: '插个小眼',
        disabled: level.value == SubscriptionLevel.Update
    },
    {
        key: SubscriptionLevel.Comment,
        label: '插个大眼',
        disabled: level.value == SubscriptionLevel.Comment
    }
]);

// 处理订阅切换
const handleSubscription = (v: number) => {
    loading.value = true;
    http.post("/subscriptions", { obj: props.obj, level: v }).then(() => {
        level.value = v;
    }).finally(() => {
        loading.value = false;
    })
};
</script>

<template>
    <n-dropdown trigger="hover" :options="options" @select="handleSubscription">
        <n-button icon-placement="right" :ghost="!level" :loading="loading" :disabled="loading">
            <template #icon>
                <n-icon>
                    <BookmarkFilled v-if="level" color="#fb7299" />
                    <BookmarkBorderFilled v-else />
                </n-icon>
            </template>
            插眼
        </n-button>
    </n-dropdown>
</template>