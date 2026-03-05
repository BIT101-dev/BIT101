<script setup lang="ts">
import { ref } from "vue";
import { SettingsOutlined } from "@vicons/material";
import store from "@/utils/store";
import { NButton, NIcon, NModal, NFormItem, NInput, NSpace } from "naive-ui";

const show = ref(false);
const localUrl = ref("");

const openModal = () => {
  localUrl.value = store.bit_login_url;
  show.value = true;
};

const save = () => {
  if (localUrl.value.lastIndexOf("/") === localUrl.value.length - 1) {
    localUrl.value = localUrl.value.slice(0, -1);
  }
  store.bit_login_url = localUrl.value;
  show.value = false;
};
</script>

<template>
  <div style="display: inline-block; margin-top: 6px">
    <n-button text @click="openModal">
      <template #icon>
        <n-icon>
          <SettingsOutlined />
        </n-icon>
      </template>
    </n-button>
    <n-modal
      v-model:show="show"
      preset="card"
      title="统一身份验证登录模块 设置"
      style="width: 400px"
    >
      <div>
        <n-form-item
          label="Login Server URL"
          :show-feedback="false"
          style="margin-bottom: 5px"
        >
          <n-input
            v-model:value="localUrl"
            placeholder="请输入 Login Server URL"
          />
        </n-form-item>
        <div style="font-size: 12px; color: #999; margin-bottom: 10px">
          开源链接:
          <a
            href="https://github.com/BIT101-dev/bit-login"
            target="_blank"
            style="color: inherit; text-decoration: underline"
            >https://github.com/BIT101-dev/bit-login</a
          >
        </div>
        <n-space justify="end">
          <n-button @click="show = false">取消</n-button>
          <n-button type="primary" @click="save">保存</n-button>
        </n-space>
      </div>
    </n-modal>
  </div>
</template>
