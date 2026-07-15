<script setup lang="ts">
import SmsOutlined from "@vicons/material/SmsOutlined";
import ShieldOutlined from "@vicons/material/ShieldOutlined";
import {
  bitLoginState,
  cancelBitLoginSms,
  submitBitLoginSms,
} from "@/utils/bit-login";

function handleKeydown(event: KeyboardEvent): void {
  if (event.key === "Enter") submitBitLoginSms();
}
</script>

<template>
  <n-modal
    :show="bitLoginState.sms.show"
    :mask-closable="false"
    :close-on-esc="false"
    :auto-focus="false"
    transform-origin="center"
  >
    <n-card class="sms-card" :bordered="false" role="dialog" aria-modal="true">
      <div class="sms-heading">
        <div class="sms-icon">
          <n-icon :size="28"><SmsOutlined /></n-icon>
        </div>
        <div>
          <h2>确认是你本人</h2>
          <p>统一身份认证需要短信验证</p>
        </div>
      </div>

      <div class="sms-phone">
        验证码已发送至 <strong>{{ bitLoginState.sms.maskedPhone }}</strong>
      </div>

      <n-input
        v-model:value="bitLoginState.sms.code"
        class="sms-input"
        size="large"
        maxlength="8"
        inputmode="numeric"
        autocomplete="one-time-code"
        placeholder="请输入短信验证码"
        :status="bitLoginState.sms.error ? 'error' : undefined"
        @keydown="handleKeydown"
        @input="bitLoginState.sms.error = ''"
      />
      <n-collapse-transition :show="Boolean(bitLoginState.sms.error)">
        <div class="sms-error">{{ bitLoginState.sms.error }}</div>
      </n-collapse-transition>

      <div class="sms-security">
        <n-icon :size="16"><ShieldOutlined /></n-icon>
        <span>验证码仅用于完成本次登录，请勿告知他人</span>
      </div>

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
  border-radius: 12px;
  box-shadow: 0 18px 54px rgba(36, 93, 107, 0.2);
}

.sms-heading {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 22px;
}

.sms-heading h2 {
  margin: 0 0 4px;
  color: var(--text-color-1);
  font-size: 21px;
  line-height: 1.2;
}

.sms-heading p {
  margin: 0;
  color: var(--text-color-3);
  font-size: 14px;
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
  margin-bottom: 12px;
  color: var(--text-color-2);
  font-size: 14px;
}

.sms-phone strong {
  color: var(--text-color-1);
}

.sms-input :deep(input) {
  font-size: 19px;
  letter-spacing: 0.18em;
}

.sms-error {
  margin-top: 7px;
  color: var(--error-color);
  font-size: 13px;
}

.sms-security {
  display: flex;
  align-items: center;
  gap: 7px;
  margin: 16px 0 22px;
  color: var(--text-color-3);
  font-size: 12px;
}
</style>
