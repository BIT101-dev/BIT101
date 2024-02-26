<!--
 * @Author: flwfdd
 * @Date: 2024-02-26 15:06:00
 * @LastEditTime: 2024-02-26 16:24:20
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import { OpenLink, opacityColor } from '@/utils/tools';
import { useThemeVars } from 'naive-ui';
import { computed } from 'vue';

const props = defineProps(['data'])

const themeVars = useThemeVars();

function RandColor() {
    const low = 0.11;
    const high = 0.24;
    return opacityColor(themeVars.value.infoColor, low + Math.random() * (high - low));
}

const billboard = computed(() => {
    let l = [[] as any, [] as any];
    for (let i = 0; i < props.data.length; i++) {
        l[i % 2].push(props.data[i]);
    }
    return l
})

</script>

<style scoped>
h2 {
    margin: 4px 0 4px 0;
    text-decoration-line: underline;
    text-decoration-color: var(--primary-color);
    color: var(--text-color-2)
}
</style>

<template>
    <n-grid x-gap="11" y-gap="11" :cols="2">
        <n-gi>
            <n-grid x-gap="11" y-gap="11" :cols="1">
                <n-gi v-for="i in billboard[0]">
                    <n-card @click="OpenLink(i['url'])" :style="{
                        'background-color': RandColor(),
                        'cursor': i['url'] ? 'pointer' : 'auto'
                    }" hoverable content-style="padding:0 11px 11px 11px;">
                        <template #cover>
                            <img :src="i['img']">
                        </template>
                        <h2>{{ i['title'] }}</h2>
                        {{ i['text'] }}
                    </n-card>
                </n-gi>
            </n-grid>
        </n-gi>
        <n-gi>
            <n-grid x-gap="11" y-gap="11" :cols="1">
                <n-gi v-for="i in billboard[1]">
                    <n-card @click="OpenLink(i['url'])" :style="{
                        'background-color': RandColor(),
                        'cursor': i['url'] ? 'pointer' : 'auto'
                    }" hoverable content-style="padding:0 11px 11px 11px;">
                        <template #cover>
                            <img :src="i['img']">
                        </template>
                        <h2>{{ i['title'] }}</h2>
                        {{ i['text'] }}
                    </n-card>
                </n-gi>
            </n-grid>
        </n-gi>
    </n-grid>
</template>


