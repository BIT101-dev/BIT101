<template>
  <n-alert :type="status?.type" title="Oops..." v-if="status">
    {{ status?.message }}
  </n-alert>
</template>

<script setup lang="ts">
import http from "@/utils/request";
import { ServiceKey, UPDATE_INTERVAL, type ServiceStatusResponse } from "@/utils/serviceStatus";
import store from "@/utils/store";
import { computed, onMounted, ref } from "vue";

const props = defineProps<{
  service: ServiceKey;
}>();

const status = computed(() => store.service_status.items[props.service])

onMounted(async () => {
  if (Date.now() - store.service_status.lastUpdated > UPDATE_INTERVAL) {
    const resp = await http.get<{ data: ServiceStatusResponse }>("/variables?obj=service_status")
    store.service_status = resp.data.data
    // const resp: ServiceStatusResponse = {
    //   lastUpdated: Date.now(),
    //   items: {
    //     [ServiceKey.Score]: {
    //       type: "error",
    //       message: "由于统一认证服务变动，暂时无法使用"
    //     }
    //   }
    // }
    // store.service_status = resp
  }

  console.debug("[ServiceStatusAlert]", store.service_status.items, props.service, status.value)
})
</script>
