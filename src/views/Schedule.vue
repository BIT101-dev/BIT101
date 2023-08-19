<!--
 * @Author: flwfdd
 * @Date: 2023-02-13 21:52:38
 * @LastEditTime: 2023-08-19 12:03:11
 * @Description: 课程表页面
 * _(:з」∠)_
-->

<script setup lang="ts">
import http from '@/utils/request';
import { WebvpnVerify, webvpn } from '@/utils/tools';
import { reactive, ref, onMounted, watch } from 'vue';

const user = reactive({
    sid: "",
    password: ""
})

const schedule = reactive({
    loading: false,
    url: '',
    msg: '',
})

function GetSchedule() {
    if (!webvpn.cookie) return;
    schedule.loading = true;
    http.get('/courses/schedule', {
        headers: {
            'webvpn-cookie': webvpn.cookie
        }
    })
        .then((res) => {
            schedule.url = res.data.url;
            schedule.msg = res.data.note;
            schedule.loading = false;
        }).catch(() => {
            schedule.loading = false;
        })
}

function Open(url: string) {
    window.open(url, '_blank');
}

onMounted(() => {
    GetSchedule();
})

watch(() => webvpn.cookie, () => {
    GetSchedule();
})

</script>

<template>
    <div class="container">
        <n-card title="课程表">
            <n-space vertical v-if="!webvpn.cookie">
                <n-input v-model:value="user.sid" type="number" placeholder="学号" />
                <n-input v-model:value="user.password" type="password" show-password-on="click" placeholder="学校统一身份认证密码" />
                <n-button @click="WebvpnVerify(user.sid, user.password)"
                    :disabled="!user.sid || !user.password || webvpn.loading" block :loading="webvpn.loading">
                    查询
                </n-button>
            </n-space>

            <div v-if="schedule.loading" style="text-align: center;">
                <n-spin size="large">
                    <template #description>
                        正在获取课程表
                    </template>
                </n-spin>
            </div>
            <div v-if="schedule.url">
                <p style="margin-top:0;">{{ schedule.msg }}</p>
                <n-button @click="Open(schedule.url)" block>
                    打开课程表
                </n-button>
            </div>

        </n-card>
        <n-alert :show-icon="false" type="info">
            导出的是当前学期的课表（.ics格式），iOS用户直接打开链接即可添加到日历，安卓用户可使用BIT101-Android APP（或支持.ics格式的日历软件）,桌面端也有软件可以适配.ics格式。具体请见：
            <a style="color:#888" target="_blank" href="/#/paper/show/21">
                使用攻略
            </a>
        </n-alert>

    </div>
</template>