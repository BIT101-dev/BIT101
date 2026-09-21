<script setup lang="ts">
import {
  bitLoginState,
  cancelBitLoginCaptcha,
  submitBitLoginCaptcha,
} from "@/utils/bit-login";

function handleKeydown(event: KeyboardEvent): void {
  if (event.key === "Enter") submitBitLoginCaptcha();
}
</script>

<template>
  <n-modal
    :show="bitLoginState.captcha.show"
    :mask-closable="false"
    :close-on-esc="false"
    :auto-focus="true"
  >
    <n-card title="图形验证码" class="captcha-card" :bordered="false" role="dialog" aria-modal="true">
      <n-space vertical>
        <n-alert type="info" :show-icon="false">
          学校统一身份认证要求完成图形验证码。验证码仅用于本次登录。
        </n-alert>
        <img
          v-if="bitLoginState.captcha.image"
          :src="bitLoginState.captcha.image"
          class="captcha-image"
          alt="统一身份认证图形验证码"
        />
        <n-input
          v-model:value="bitLoginState.captcha.code"
          placeholder="请输入图中的验证码"
          maxlength="16"
          :status="bitLoginState.captcha.error ? 'error' : undefined"
          @input="bitLoginState.captcha.error = ''"
          @keydown="handleKeydown"
        />
        <div v-if="bitLoginState.captcha.error" class="captcha-error">
          {{ bitLoginState.captcha.error }}
        </div>
      </n-space>
      <template #footer>
        <n-space justify="end">
          <n-button @click="cancelBitLoginCaptcha">取消</n-button>
          <n-button type="primary" :disabled="!bitLoginState.captcha.code" @click="submitBitLoginCaptcha">
            继续
          </n-button>
        </n-space>
      </template>
    </n-card>
  </n-modal>
</template>

<style scoped>
.captcha-card {
  width: min(420px, calc(100vw - 32px));
}

.captcha-image {
  display: block;
  max-width: 100%;
  max-height: 160px;
  margin: 4px auto;
  object-fit: contain;
}

.captcha-error {
  color: var(--error-color);
  font-size: 14px;
}
</style>
