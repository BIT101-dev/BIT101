<!--
 * @Author: flwfdd
 * @Date: 2023-02-13 21:52:38
 * @LastEditTime: 2024-02-26 17:17:45
 * @Description: 课程表页面
 * _(:з」∠)_
-->

<script setup lang="ts">
import { bitLoginRequest, bitLoginState } from "@/utils/bit-login";
import { OpenLink } from "@/utils/tools";
import { reactive } from "vue";
import BitLoginSetting from "@/components/BitLoginSetting.vue";

const user = reactive({
  sid: "",
  password: "",
  phone: "",
  authMethod: "sms" as "password" | "sms",
});

const schedule = reactive({
  loading: false,
  term: "",
  url: "",
  msg: "",
});

function GetSchedule() {
  schedule.loading = true;
  bitLoginRequest<{ url: string; note: string }>(
    {
      username: user.sid,
      password: user.password,
      phone: user.phone,
      authMethod: user.authMethod,
    },
    ["jxzxehall"],
    "/api/jxzxehall/schedule_ics",
    { kksj: schedule.term }
  )
    .then((res) => {
      schedule.url = res.data.url;
      schedule.msg = res.data.note;
      schedule.loading = false;
    })
    .catch(() => {
      schedule.loading = false;
    });
}
</script>

<template>
  <div class="container">
    <n-card title="课程表">
      <template #header-extra>
        <BitLoginSetting />
      </template>
      <n-space vertical v-if="!schedule.url">
        <n-input v-model:value="user.sid" type="number" placeholder="学号" />
        <n-radio-group v-model:value="user.authMethod" name="auth-method">
          <n-space>
            <n-radio value="sms">短信验证码（推荐）</n-radio>
            <n-radio value="password">用户名密码</n-radio>
          </n-space>
        </n-radio-group>
        <n-input
          v-if="user.authMethod === 'password'"
          v-model:value="user.password"
          type="password"
          show-password-on="click"
          placeholder="学校统一身份认证密码"
        />
        <n-input
          v-else
          v-model:value="user.phone"
          type="text"
          maxlength="11"
          placeholder="统一身份认证绑定手机号"
        />
        <n-collapse>
          <n-collapse-item title="指定学期">
            <n-input
              v-model:value="schedule.term"
              type="text"
              placeholder="如2023-2024-2 默认为当前学期"
            />
          </n-collapse-item>
        </n-collapse>

        <n-button
          @click="GetSchedule"
          :disabled="!user.sid || (user.authMethod === 'password' ? !user.password : !/^1\d{10}$/.test(user.phone))"
          block
          :loading="schedule.loading || bitLoginState.loading"
        >
          查询
        </n-button>
      </n-space>

      <!-- <div v-if="schedule.loading" style="text-align: center">
        <n-spin size="large">
          <template #description> 正在获取课程表 </template>
        </n-spin>
      </div> -->
      <div v-if="schedule.url">
        <p style="margin-top: 0">{{ schedule.msg }}</p>
        <n-button @click="OpenLink(schedule.url)" block> 打开课程表 </n-button>
      </div>
    </n-card>
    <n-alert :show-icon="false" type="info">
      导出的是当前学期的课表（.ics格式），iOS用户直接打开链接即可添加到日历，安卓用户可使用BIT101-Android
      APP（或支持.ics格式的日历软件）,桌面端也有软件可以适配.ics格式。具体请见：
      <n-a href="/paper/21"> 使用攻略 </n-a>
    </n-alert>
  </div>
</template>
