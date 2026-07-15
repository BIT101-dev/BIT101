<script setup lang="ts">
import { computed } from "vue";
import ShieldOutlined from "@vicons/material/ShieldOutlined";
import {
  bitLoginState,
  cancelBitLoginSms,
  submitBitLoginSms,
} from "@/utils/bit-login";

const smsCode = computed<string[]>({
  get: () => bitLoginState.sms.code.split(""),
  set: (value) => {
    bitLoginState.sms.code = value.join("");
    bitLoginState.sms.error = "";
  },
});

function handleKeydown(event: KeyboardEvent): void {
  if (event.key === "Enter") submitBitLoginSms();
}
</script>

<template>
  <n-modal
    :show="bitLoginState.sms.show"
    :mask-closable="false"
    :close-on-esc="false"
    :auto-focus="true"
    transform-origin="center"
  >
    <n-card title="确 认 是 你 本 人" class="sms-card" :bordered="false" role="dialog" aria-modal="true">
      <n-space vertical>
        <div class="sms-security">
          <n-icon :size="16"><ShieldOutlined /></n-icon>
          <span>验证码仅用于完成本次登录，请勿告知他人。</span>
        </div>
        
        <div class="sms-phone">
          验证码已发送至 <strong>{{ bitLoginState.sms.maskedPhone }}</strong>
        </div>

        <n-input-otp
          v-model:value="smsCode"
          class="sms-input"
          :length="6"
          size="large"
          :allow-input="(value: string) => !value || /^\d+$/.test(value)"
          :status="bitLoginState.sms.error ? 'error' : undefined"
          @keydown="handleKeydown"
        />
        
        <n-collapse-transition :show="Boolean(bitLoginState.sms.error)">
          <div class="sms-error">{{ bitLoginState.sms.error }}</div>
        </n-collapse-transition>

        <n-p class="acknowledgement">您的登录凭证仅供当前会话使用，BIT101 承诺不会在服务端留存您的凭证信息。</n-p>
        <n-p class="acknowledgement">如果您正在遭遇电信诈骗，请拨打校内全天应急电话 <n-a href="tel:010-68916110">010-68916110</n-a>。</n-p>
      </n-space>

      <n-space justify="end">
        <n-button @click="cancelBitLoginSms">
          取消
        </n-button>
        <n-button type="primary" :disabled="!bitLoginState.sms.code" @click="submitBitLoginSms">
          继续验证
        </n-button>
      </n-space>
    </n-card>
  </n-modal>
</template>

<style scoped>
.sms-card {
  width: min(420px, calc(100vw - 32px));
}

.sms-icon {
  display: grid;
  width: 50px;
  height: 50px;
  flex: 0 0 50px;
  place-items: center;
  border-radius: 14px;
  color: var(--primary-color);
  background: color-mix(in srgb, var(--primary-color) 15%, transparent);
}

.sms-phone {
  color: var(--text-color-2);
  font-size: 14px;
}

.sms-phone strong {
  color: var(--text-color-1);
}

.sms-error {
  color: var(--error-color);
}

.sms-security {
  display: flex;
  align-items: center;
  gap: 7px;
  color: var(--text-color-3);
  font-size: 14px;
}

.acknowledgement {
  color: var(--text-color-3);
  font-size: 14px;
}
</style>
