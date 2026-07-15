<script setup lang="ts">
import SaveFilled from "@vicons/material/SaveFilled";
import http from "@/utils/request";
import {
  ServiceKey,
  type ServiceStatusData,
  type ServiceStatusItems,
} from "@/utils/serviceStatus";
import type { FormInst, FormRules } from "naive-ui";
import { onMounted, reactive, ref } from "vue";

const services = Object.values(ServiceKey) as ServiceKey[];

const typeOptions = [
  { label: "提示", value: "info" },
  { label: "警告", value: "warning" },
  { label: "错误", value: "error" },
];

const statusItems = reactive<ServiceStatusItems>({});
const formRef = ref<FormInst | null>(null);
const loading = ref(false);
const submitting = ref(false);
const rules: FormRules = Object.fromEntries(
  services.map((key) => [
    `${key}.message`,
    {
      required: true,
      message: "请输入通知内容",
      trigger: ["input", "blur"],
    },
  ])
);

function setEnabled(key: ServiceKey, enabled: boolean) {
  if (enabled) {
    statusItems[key] ??= { type: "info", message: "" };
  } else {
    delete statusItems[key];
  }
}

function setType(key: ServiceKey, type: ServiceStatusData["type"]) {
  const item = statusItems[key];
  if (item) item.type = type;
}

function setMessage(key: ServiceKey, message: string) {
  const item = statusItems[key];
  if (item) item.message = message;
}

async function load() {
  loading.value = true;
  try {
    const res = await http.get("/variables?obj=service_status");
    const items = JSON.parse(res.data.data) as ServiceStatusItems;

    Object.keys(statusItems).forEach((key) => {
      delete statusItems[key as ServiceKey];
    });
    Object.assign(statusItems, items);
  } finally {
    loading.value = false;
  }
}

async function submit() {
  await formRef.value?.validate();
  submitting.value = true;
  try {
    await http.post("/variables", {
      obj: "service_status",
      data: JSON.stringify(statusItems),
    });
  } finally {
    submitting.value = false;
  }
}

onMounted(load);
</script>

<template>
  <div class="container">
    <n-space vertical>
      <h2>服务状态通知</h2>

      <n-spin :show="loading">
        <n-form ref="formRef" :model="statusItems" :rules="rules" label-placement="left" label-width="90">
          <n-space vertical>
            <n-card v-for="service in services" :key="service" :title="service">
              <n-form-item label="显示通知">
                <n-switch
                  :value="Boolean(statusItems[service])"
                  @update:value="setEnabled(service, $event)" />
              </n-form-item>

              <n-collapse-transition :show="statusItems[service] !== undefined">
                <n-form-item label="通知等级" :path="`${service}.type`">
                  <n-select
                    :value="statusItems[service]?.type"
                    :options="typeOptions"
                    @update:value="setType(service, $event as ServiceStatusData['type'])"
                  />
                </n-form-item>
                <n-form-item label="通知内容" :path="`${service}.message`">
                  <n-input
                    :value="statusItems[service]?.message"
                    type="textarea"
                    placeholder="请输入通知内容"
                    @update:value="setMessage(service, $event)"
                  />
                </n-form-item>
              </n-collapse-transition>
            </n-card>
          </n-space>
        </n-form>
      </n-spin>

      <n-button :loading="submitting" :disabled="loading" @click="submit" style="width: 100%">
        <template #icon>
          <SaveFilled />
        </template>
        保存
      </n-button>
    </n-space>
  </div>
</template>
