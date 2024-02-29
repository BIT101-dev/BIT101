<script setup lang="ts">
import { defineProps, reactive, defineEmits } from 'vue';
import { useThemeVars } from 'naive-ui'

const props = defineProps({
  src: {
    type: String,
    required: true
  },
  lazy: {
    type: Boolean,
    default: true
  }
})

const emits = defineEmits(["preview"])

const open = () => {
  emits("preview")
}

const containerStyle = reactive({
  width: "100%",
  height: "100%",
  position: "absolute",
  top: 0,
  left: 0,
  "object-fit": "contain",
  background: useThemeVars().value.actionColor,
  "aspect-radio": "1/1",
  "border-radius": useThemeVars().value.borderRadius,
  border: `1px solid ${useThemeVars().value.borderColor}`,
  "box-sizing": "border-box"
})

const picStyle = reactive({
  width: "100%",
  height: "100%",
  "aspect-radio": "1/1",
  "object-fit": "cover",
  "user-drag": "none",
  "user-select": "none",
  "border-radius": useThemeVars().value.borderRadiusSmall,
})
</script>

<template>
  <n-element :style="containerStyle" @click.stop="(e: MouseEvent) => {
      e.preventDefault()
      open()
    }">
    <!-- @vue-ignore-error -->
    <img :src="props.src" :style="picStyle" :lazy="props.lazy" onerror="this.style.display = 'none'"/>
  </n-element>
</template>