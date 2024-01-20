<script setup lang="ts">
import { OpenLink } from '@/utils/tools';
import { computed } from 'vue';

const props = defineProps(['data'])

function RandColor() {
    let h = 192, s = 11 + Math.random() * 24, v = 100;
    s = s / 100;
    v = v / 100;
    let r = 0, g = 0, b = 0;
    let i = Math.floor(h / 60) % 6;
    let f = h / 60 - i;
    let p = v * (1 - s);
    let q = v * (1 - f * s);
    let t = v * (1 - (1 - f) * s);
    switch (i) {
        case 0:
            r = v; g = t; b = p;
            break;
        case 1:
            r = q; g = v; b = p;
            break;
        case 2:
            r = p; g = v; b = t;
            break;
        case 3:
            r = p; g = q; b = v;
            break;
        case 4:
            r = t; g = p; b = v;
            break;
        case 5:
            r = v; g = p; b = q;
            break;
        default:
            break;
    }
    r = r * 255.0;
    g = g * 255.0;
    b = b * 255.0;
    return `rgba(${r},${g},${b},100)`
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
    text-decoration-color: var(--primary);
}
</style>

<template>
    <n-grid x-gap="11" y-gap="11" :cols="2">
        <n-gi>
            <n-grid x-gap="11" y-gap="11" :cols="1">
                <n-gi v-for="i in billboard[0]">
                    <n-card @click="OpenLink(i['url'])"
                        :style="{
                            'background-color': RandColor(),
                            'cursor': i['url'] ? 'pointer' : 'auto',
                            'color': 'rgb(51, 54, 57)'
                        }"
                        hoverable
                        content-style="padding:0 11px 11px 11px;">
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
                    <n-card @click="OpenLink(i['url'])"
                        :style="{
                            'background-color': RandColor(),
                            'cursor': i['url'] ? 'pointer' : 'auto',
                            'color': 'rgb(51, 54, 57)'
                        }"
                        hoverable
                        content-style="padding:0 11px 11px 11px;">
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


