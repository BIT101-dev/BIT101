<script lang="ts" setup>
import { ref, PropType } from 'vue';
const openModal = ref(false)
const position = ref(0)

const props = defineProps({
  images: {
    type: Object as PropType<{
      low_url: string,
      mid: string,
      url: string
    }[]>
  },
  lazy: {
    type: Boolean,
    default: true
  }
})

const showModal = (idx: number) => {
  position.value = idx
  openModal.value = true
}
</script>

<template>
  <n-grid x-gap="5" y-gap="5" :cols="3" style="max-width: 424px;">
    <n-gi v-for="(image, idx) in props.images">
      <div v-if="idx <= 2" @click.stop="" style="height: 0; padding-bottom:  100%; position: relative;">
        <ImageBox :src="image.low_url" lazy @preview="showModal(idx)" />
        <div v-if="idx == 2 && props.images!.length > 3"
          style="width: 100%; height: 100% ;position:absolute;border-radius:3px;background-color:rgba(0,0,0,0.5);display:flex; justify-content:center;align-items:center;pointer-events:none;">
          <h2 style="color:#fff">+{{ props.images!.length - 2 }}</h2>
        </div>
      </div>
    </n-gi>
  </n-grid>
  <n-modal :show="openModal" :auto-focus="false">
    <ImageModal :src="props.images![position].url" :idx="position" :amount="props.images!.length"
      @close="() => openModal = false" @prev="() => position -= 1" @next="() => position += 1" />
  </n-modal>
</template>

