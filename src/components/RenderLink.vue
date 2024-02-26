<!--
 * @Author: flwfdd
 * @Date: 2023-10-24 11:52:42
 * @LastEditTime: 2024-02-26 17:02:09
 * @Description: _(:з」∠)_
-->
<script setup lang="ts">
import { onMounted, reactive } from 'vue';

const origin=window.location.origin;

const props = defineProps({
  value: {
    type: String,
    required: true
  },
})

interface Node {
  type: 'text' | 'link',
  text: string
}

const list = reactive([] as Node[])

onMounted(() => {
  let rex = /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/g;
  let matches = [...props.value.matchAll(rex)];
  let last = 0;
  if (matches.length) {
    for (let match of matches) {
      if (match.index!! > last) {
        list.push({
          type: 'text',
          text: props.value.slice(last, match.index)
        })
      }
      list.push({
        type: 'link',
        text: match[0]
      })
      last = match.index!! + match[0].length;
    }
    if (last < props.value.length) {
      list.push({
        type: 'text',
        text: props.value.slice(last)
      })
    }
  } else list.push({
    type: 'text',
    text: props.value
  })
})

</script>

<template>
  <template v-for="i in list">
    <template v-if="i.type == 'text'">
      {{ i.text }}
    </template>
    <a v-if="i.type == 'link'" :href="i.text" :target="i.text.startsWith(origin)?'_self':'_blank'" style="text-decoration:none;color:var(--primary-color)">{{ i.text }}</a>
  </template>
</template>