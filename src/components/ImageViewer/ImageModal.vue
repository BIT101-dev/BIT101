<script setup lang="ts">
import { defineProps, reactive, defineEmits, ref, watch, StyleValue, onUpdated } from 'vue';
import { onBeforeRouteLeave } from 'vue-router'
import ArrowForwardFilled from '@vicons/material/ArrowForwardFilled'
import ArrowBackFilled from '@vicons/material/ArrowBackFilled'
import BrokenImageFilled from '@vicons/material/BrokenImageFilled'
import CloseFilled from '@vicons/material/CloseFilled'
import DownloadFilled from '@vicons/material/DownloadFilled'
import { useThemeVars } from 'naive-ui'
import './ImageModal.css'

const props = defineProps({
  src: {
    type: String,
    required: true,
  },
  idx: {
    type: Number,
    default: 0
  },
  amount: {
    type: Number,
    default: 1
  }
})

const containerStyle = reactive({
  background: "transparent",
  position: "absolute",
  left: "0px",
  right: "0px",
  top: "0px",
  bottom: "0px",
  display: "flex",
  "align-self": "unset",
  "align-items": "center",
  "justify-content": "center",
  overflow: "hidden"
})

const baseStyle = reactive({
  "object-fit": "contain",
  "max-height": "100vh",
  "max-width": "100vw",
  "user-select": "none",
  "user-drag": "none"
})

const button = reactive({
  position: "absolute",
  color: useThemeVars().value.iconColor,
  background: "rgba(255, 255, 255, 0.2)"
})
const leftButton = reactive({
  left: "8px"
})

const rightButton = reactive({
  right: "8px"
})

const topButton = reactive({
  top: "8px"
})

const bottomButton = reactive({
  bottom: "8px"
})

const picStyle = ref<{ [k: string]: string }[]>([baseStyle])

const load = ref(false)
const loadError = ref(false)

const loadingStyle = ref([{ display: "none" }])
watch(load, () => {
  if (load.value && !loadError.value) {
    loadingStyle.value = [{ display: "block" }]
  }
  else {
    loadingStyle.value = [{ display: "none" }]
  }
})

const emits = defineEmits(["close", "prev", "next"])
const close = () => emits("close")
const prev = () => emits("prev")
const next = () => emits("next")
const download = async () => {
  if (load.value && !loadError.value) {
    window.$message.info("开始下载啦!")
    try {
      const pic = await (await fetch(props.src, { mode: 'no-cors' })).blob()
      const a = document.createElement("a")
      a.href = window.URL.createObjectURL(pic)
      a.download = props.src.match(/[^\/]*\.[^\/]{1,6}$/)![0]
      a.click()
      window.$message.success("下载成功\\^v^/")
    }
    catch {
      window.$message.error("下载出错qwq")
    }
  }
}

let touch: TouchList
let start = false
let scale = false
let thisTimeScaled = false
let scaleCenter: { centerX: number, centerY: number, distance: number } = { centerX: 0, centerY: 0, distance: 0 }
const distance = (a: Touch, b: Touch) => Math.sqrt((a.clientX - b.clientX) ** 2 + (a.clientY - b.clientY) ** 2)

const touchStart = (e: TouchEvent) => {
  touch = e.touches
  start = true

  if (touch.length === 2) {
    scale = true
    scaleCenter.centerX = (e.touches[0].clientX + e.touches[1].clientX) / 2
    scaleCenter.centerY = (e.touches[0].clientY + e.touches[1].clientY) / 2
    scaleCenter.distance = distance(e.touches[0], e.touches[1])
  }
}
const touchEventHandler = (e: TouchEvent) => {
  if (e.touches.length === 1) {
    // 单点触控
    let clientX = e.touches[0].clientX
    let clientY = e.touches[0].clientY

    let { clientX: startX, clientY: startY } = touch[0]

    if (!scale) {
      // 未缩放, 切换
      switchPic(clientX, startX)
      return
    }

    else if (!thisTimeScaled) {
      // 平移
      movePic(clientX, clientY, startX, startY)
    }
  }

  if (e.touches.length === 2) {
    // 这次缩放了 不能平移
    thisTimeScaled = true
    scalePic(distance(e.touches[0], e.touches[1]))
  }
}

const animation = ref<"slide-fade-left" | "slide-fade-right">("slide-fade-right")
const switchPic = async (clientX: number, startX: number, distance: number = 50) => {
  if (clientX - startX < -distance && props.idx + 1 !== props.amount && start)
    next()
  if (clientX - startX > distance && props.idx !== 0 && start)
    prev()
}

let offsetX = 0, offsetY = 0
let displayOffsetX = 0, displayOffsetY = 0
let reactiveOffsetX = ref("0")
let reactiveOffsetY = ref("0")
const movePic = (clientX: number, clientY: number, startX: number, startY: number) => {
  offsetX = clientX - startX + displayOffsetX
  offsetY = clientY - startY + displayOffsetY

  reactiveOffsetX.value = offsetX.toString() + "px"
  reactiveOffsetY.value = offsetY.toString() + "px"
}

let displayRatio = 100
let ratio = 100
let transform = ref("scale(100%)")
const scalePic = (distance: number) => {
  ratio = distance / scaleCenter.distance

  let vh = window.innerHeight / 100
  let vw = window.innerWidth / 100

  // 玄学 缩放的时候进行偏移 让缩放后内容在手底下
  offsetX = (50 * vw - scaleCenter.centerX) * (ratio - 1) + displayOffsetX
  offsetY = (50 * vh - scaleCenter.centerY) * (ratio - 1) + displayOffsetY

  reactiveOffsetX.value = offsetX.toString() + "px"
  reactiveOffsetY.value = offsetY.toString() + "px"

  ratio *= displayRatio;
  ratio = ratio > 100 ? ratio : 100;
  transform.value = `scale(${ratio}%)`
}

const touchEndHandler = (e: TouchEvent) => {
  thisTimeScaled = e.touches.length >= 1
  operationCleanUp()
}

const operationCleanUp = () => {
  if (scale) {
    displayRatio = ratio
    displayOffsetX = offsetX
    displayOffsetY = offsetY

    if (displayRatio === 100) {
      scale = false
      transform.value = ""
      displayOffsetX = 0, displayOffsetY = 0
      picStyle.value = [baseStyle, transition]
      reactiveOffsetX.value = "0px"
      reactiveOffsetY.value = "0px"
      setTimeout(() => picStyle.value = [baseStyle], 133)
    }
  }
}

const wheelEventHandler = (e: WheelEvent) => {
  e.preventDefault()
  if (e.deltaY !== 0) {
    scale = true

    scaleCenter.centerX = e.clientX
    scaleCenter.centerY = e.clientY
    scaleCenter.distance = 1

    scalePic(-e.deltaY / 100 + 1)

    operationCleanUp()
  }
}

let drag: MouseEvent
const dragStart = (e: MouseEvent) => {
  start = true
  drag = e
}

const dragEventHandler = (e: MouseEvent) => {
  if (start && scale) {
    movePic(e.clientX, e.clientY, drag.clientX, drag.clientY)
  }
  if (start && !scale) {
    switchPic(e.clientX, drag.clientX, 100)
  }
}

const dragEndHandler = () => {
  start = false
  operationCleanUp()
}

const transition = {
  transition: "0.133s ease-out"
}

const transformStyle = reactive({
  transform,
  "position": "relative",
  "top": reactiveOffsetY,
  "left": reactiveOffsetX
}) as StyleValue

onBeforeRouteLeave((to, from) => {
  close()
  return false
})

const prevIdx = ref(0)
onUpdated(() => {
  // 重置加载状态
  start = false
  load.value = false
  loadError.value = false

  // 动画
  animation.value = props.idx < prevIdx.value ? "slide-fade-left" : "slide-fade-right"
  prevIdx.value = props.idx
})
</script>

<template>
  <n-element :style="containerStyle" @click="() => close()" @mousedown.stop="dragStart"
    @mousemove.stop="dragEventHandler" @mouseup.stop="dragEndHandler" @touchstart.stop="touchStart"
    @touchmove.stop="touchEventHandler" @touchend.stop="touchEndHandler" @wheel.stop="wheelEventHandler">
    <div style="max-height: 100%; max-width: 100%; display: flex; align-items: center; justify-content: center;">
      <Transition :name="animation" mode="out-in">
        <!-- @vue-ignore-error -->
        <img :key="props.idx" :src="props.src" :style="[picStyle, transformStyle, loadingStyle]" draggable="false"
          @error="() => { loadError = true; load = true }" @load="() => load = true" @click.stop />
      </Transition>
      <n-empty v-if="loadError" description="加载不出来了啦" style="--n-text-color: #ffffff">
        <template #icon>
          <n-icon>
            <BrokenImageFilled style="color: #ffffff" />
          </n-icon>
        </template>
        <template #extra>
          <n-button style="color: #ffffff">再试试</n-button>
        </template>
      </n-empty>
      <n-spin v-if="!load" />
    </div>
    <n-button @click.stop="prev()" circle v-if="props.amount > 1 && props.idx !== 0" :style="[button, leftButton]">
      <template #icon>
        <n-icon>
          <ArrowBackFilled />
        </n-icon>
      </template>
    </n-button>
    <n-button @click.stop="next()" circle v-if="props.amount > 1 && props.idx + 1 !== props.amount"
      :style="[button, rightButton]">
      <template #icon>
        <n-icon>
          <ArrowForwardFilled />
        </n-icon>
      </template>
    </n-button>
    <n-button @click.stop="close()" circle :style="[button, rightButton, topButton]">
      <template #icon>
        <n-icon>
          <CloseFilled />
        </n-icon>
      </template>
    </n-button>
    <n-button @click.stop="download()" circle :style="[button, rightButton, bottomButton]">
      <template #icon>
        <n-icon>
          <DownloadFilled />
        </n-icon>
      </template>
    </n-button>
  </n-element>
</template>