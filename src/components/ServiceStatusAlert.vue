<template>
  <n-alert :type="status?.type" title="Oops..." v-if="status">
    {{ status?.message }}
  </n-alert>
</template>

<script setup lang="ts">
import http from "@/utils/request";
import { ServiceKey, ServiceStatusItems, UPDATE_INTERVAL, type ServiceStatusResponse } from "@/utils/serviceStatus";
import store from "@/utils/store";
import { computed, onMounted, ref } from "vue";

const props = defineProps<{
  service: ServiceKey;
}>();

const status = computed(() => store.service_status.items[props.service])

onMounted(async () => {
  if (Date.now() - store.service_status.lastUpdated > UPDATE_INTERVAL) {
    const resp = await http.get("/variables?obj=service_status")
    const result: ServiceStatusItems | null = JSON.parse(resp.data.data)
    if (result) {
      store.service_status = {
        lastUpdated: Date.now(),
        items: result,
      }
    }
  }

  console.debug("[ServiceStatusAlert]", store.service_status.items, props.service, status.value)
})
</script>
