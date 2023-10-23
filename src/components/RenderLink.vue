<script setup lang="ts">
import { onMounted, reactive } from 'vue';


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
  } else list.push({
    type: 'text',
    text: props.value
  })
  console.log(list);
})

</script>

<template>
  <template v-for="i in list">
    <template v-if="i.type == 'text'">
      {{ i.text }}
    </template>
    <a v-if="i.type=='link'" :href="i.text" target="_blank" style="text-decoration:none;color:#FF8533">{{ i.text }}</a>
  </template>
</template>