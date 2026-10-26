<!--
 * @Author: flwfdd
 * @Date: 2023-02-13 21:52:38
 * @LastEditTime: 2024-02-26 17:17:45
 * @Description: 课程表页面
 * _(:з」∠)_
-->

<script setup lang="ts">
import http from "@/utils/request";
import { hasSchoolCookie, isSchoolAuthRequired, schoolSession, withSchoolSession } from "@/utils/school";
import { clearSchoolResults, readSchoolCache, resultKey, writeSchoolCache } from "@/utils/school-cache";
import { FormatTime } from "@/utils/tools";
import store from "@/utils/store";
import { onMounted, reactive, ref, watch } from "vue";

const user = reactive({
  sid: store.grade_query.sid || schoolSession.sid || "",
  password: "",
});

const savedTerm = readSchoolCache<string>("schedule-term")?.data;
const schedule = reactive({
  loading: false,
  term: typeof savedTerm === "string" ? savedTerm : "",
  content: "",
  msg: "",
  cachedAt: 0,
});
const show_form = ref(true);
const scheduleGeneration = ref(0);

function RestoreSchedule(): boolean {
  const key = resultKey("schedule", user.sid.trim(), schedule.term.trim() || "current");
  const cached = readSchoolCache<{ note: string; content: string }>(key);
  if (!cached || typeof cached.data.content !== "string" ||
    !cached.data.content.includes("BEGIN:VCALENDAR") ||
    !cached.data.content.includes("END:VCALENDAR")) {
    schedule.content = "";
    schedule.msg = "";
    schedule.cachedAt = 0;
    show_form.value = true;
    return false;
  }
  schedule.content = cached.data.content;
  schedule.msg = cached.data.note;
  schedule.cachedAt = cached.cachedAt;
  show_form.value = false;
  return true;
}

async function GetSchedule(username: string, password: string) {
  schedule.loading = true;
  const sid = username.trim();
  const term = schedule.term.trim();
  const generation = scheduleGeneration.value;
  try {
    const res = await withSchoolSession(sid, password, (cookie) => http.get("/courses/schedule", {
      params: { term },
      headers: { "webvpn-cookie": cookie },
    }));
    const response = await fetch(new URL(res.data.url, store.api_url), { credentials: "omit" });
    if (!response.ok) throw new Error("下载课程表失败");
    const content = await response.text();
    if (!content.includes("BEGIN:VCALENDAR") || !content.includes("END:VCALENDAR")) {
      throw new Error("课程表内容无效");
    }
    if (generation !== scheduleGeneration.value || user.sid.trim() !== sid || schedule.term.trim() !== term) return;
    schedule.term = term;
    schedule.content = content;
    schedule.msg = res.data.note;
    schedule.cachedAt = Math.floor(Date.now() / 1000);
    store.grade_query.sid = sid;
    writeSchoolCache(resultKey("schedule", sid, term || "current"), {
      note: schedule.msg,
      content,
    });
    show_form.value = false;
  } catch (error: any) {
    if (isSchoolAuthRequired(error)) show_form.value = true;
    if (!error?.response && !error?.__bit101Notified) window.$message.error(error?.message || "获取课表失败");
  } finally {
    schedule.loading = false;
  }
}

function OpenSchedule() {
  const blob = new Blob([schedule.content], { type: "text/calendar;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `BIT101-${schedule.term || "current"}.ics`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function ClearScheduleCache() {
  scheduleGeneration.value++;
  clearSchoolResults("schedule", user.sid.trim());
  schedule.content = "";
  schedule.msg = "";
  schedule.cachedAt = 0;
  show_form.value = true;
  window.$message.success("已清除本地课表缓存");
}

onMounted(() => {
  RestoreSchedule();
});

watch([() => user.sid, () => schedule.term], () => {
  scheduleGeneration.value++;
  writeSchoolCache("schedule-term", schedule.term.trim());
  RestoreSchedule();
});

watch(() => schoolSession.cookie, (value, previous) => {
  if (previous && !value) user.password = "";
});
</script>

<template>
  <div class="container">
    <n-card title="课程表">
      <n-space vertical v-if="show_form">
        <n-input
          v-model:value="user.sid"
          type="number"
          placeholder="学号"
          :disabled="schedule.loading || schoolSession.loading"
        />
        <n-input
          v-model:value="user.password"
          type="password"
          show-password-on="click"
          placeholder="学校统一身份认证密码"
          :disabled="schedule.loading || schoolSession.loading"
        />
        <p v-if="hasSchoolCookie(user.sid)">已有学校会话，密码可留空。</p>
        <n-collapse>
          <n-collapse-item title="指定学期">
            <n-input
              v-model:value="schedule.term"
              type="text"
              placeholder="如2023-2024-2 默认为当前学期"
              :disabled="schedule.loading || schoolSession.loading"
            />
          </n-collapse-item>
        </n-collapse>

        <n-button
          @click="GetSchedule(user.sid, user.password)"
          :disabled="!user.sid || (!user.password && !hasSchoolCookie(user.sid)) || schedule.loading || schoolSession.loading"
          block
          :loading="schedule.loading || schoolSession.loading"
        >
          查询
        </n-button>
      </n-space>

      <n-space vertical v-if="schedule.content" :size="12" style="margin-top: 12px">
        <p style="margin-top: 0">{{ schedule.msg }}</p>
        <p v-if="schedule.cachedAt">上次更新：{{ FormatTime(schedule.cachedAt) }}</p>
        <n-button @click="OpenSchedule" block>打开课程表</n-button>
        <n-button @click="show_form = true" :disabled="schedule.loading || schoolSession.loading" block>
          刷新 / 重新查询
        </n-button>
        <n-button @click="ClearScheduleCache" :disabled="schedule.loading || schoolSession.loading" block>
          清除本地缓存
        </n-button>
      </n-space>
    </n-card>
    <n-alert :show-icon="false" type="info">
      导出的是当前学期的课表（.ics格式），iOS用户直接打开链接即可添加到日历，安卓用户可使用BIT101-Android
      APP（或支持.ics格式的日历软件）,桌面端也有软件可以适配.ics格式。具体请见：
      <n-a href="/paper/21"> 使用攻略 </n-a>
    </n-alert>
  </div>
</template>
