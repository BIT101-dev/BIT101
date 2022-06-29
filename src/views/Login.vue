<!--
 * @Author: flwfdd
 * @Date: 2022-05-28 01:26:29
 * @LastEditTime: 2022-06-28 20:57:21
 * @Description: 用户登陆注册页面
 * _(:з」∠)_
-->
<script setup lang="ts">
import { hitokoto } from '@/utils/tools';
import { onMounted, reactive, ref } from 'vue';
import { FormRules, FormItemRule, FormInst } from 'naive-ui';
import http from '@/utils/request';
import { Md5 } from "ts-md5/dist/md5"
import store from '@/utils/store';
import {webvpn,WebvpnVerify} from '@/utils/tools'

const user = reactive({
    sid: "",
    password: "",
    repassword: "",
    verify_type: "webvpn",
    verify_code: "",
    webvpn_password: "",
})

const form_ref = ref<FormInst | null>(null);
const rules: FormRules = {
    sid: [
        {
            required: true,
            validator(rule: FormItemRule, value: string) {
                if (!value) {
                    return new Error('空空如也呢')
                } else if (!/^\d*$/.test(value)) {
                    return new Error('不大对劲')
                }
                return true
            },
            trigger: ['input', 'blur']
        }
    ],
    password: [
        {
            required: true,
            validator(rule: FormItemRule, value: string) {
                if (value.length < 8) {
                    return new Error('别那么小气嘛')
                }
                return true
            },
            trigger: ['input', 'blur']
        }
    ],
    repassword: [
        {
            required: true,
            validator(rule: FormItemRule, value: string) {
                if (value != user.password) {
                    return new Error('出尔反尔可不好')
                }
                return true
            },
            trigger: ['input', 'blur']
        }
    ],
    verify_code: [
        {
            required: true,
            validator(rule: FormItemRule, value: string) {
                if ((!/^\d*$/.test(value)) || value.length != 6) {
                    return new Error('我想应该是6位的')
                }
                return true
            },
            trigger: ['input', 'blur']
        }
    ],
}

// 登陆状态
const status = ref(false);
function CheckStatus() {
    http.get('/')
        .then(() => {
            status.value = true;
        })
        .catch(() => {
            status.value = false;
        })
}

const count_down = ref(0); //倒计时
function MailVerify() {
    http.get('/user/mail_verify/?sid=' + user.sid)
        .then(() => {
            count_down.value = 60;
            let itv = setInterval(() => {
                count_down.value--;
                if (!count_down.value) clearInterval(itv);
            }, 1000);
        })
}

function Login() {
    form_ref.value?.validate((err) => {
        if (!err) {
            http.get('/user/login/', {
                params: {
                    sid: user.sid,
                    password: Md5.hashStr(user.password)
                }
            }).then(res => {
                store.fake_cookie = res.data.fake_cookie;
                CheckStatus();
            })
        } else {
            console.log(err)
            window.$message.error('请检查输入qwq')
        }
    })
}

function Register() {
    form_ref.value?.validate((err) => {
        if (!err) {
            http.get('/user/register/', {
                params: {
                    sid: user.sid,
                    password: Md5.hashStr(user.password),
                    verify_code: user.verify_code
                }
            }).then((res) => {
                store.fake_cookie = res.data.fake_cookie;
                CheckStatus();
            })
        } else {
            console.log(err)
            window.$message.error('请检查输入qwq')
        }
    })
}

onMounted(() => { CheckStatus(); })

function Logout() { store.fake_cookie = ""; CheckStatus(); }

</script>

<template>
    <div class="container">
        <n-card size="small">
            <n-alert :show-icon="false" :type="status ? 'success' : 'error'" title="此时此刻">
                <template v-if="status">
                    已登录<br />
                    抑或你想<n-button @click="Logout" text type="primary">注销</n-button>
                </template>
                <template v-else>
                    未登录
                </template>
            </n-alert>
            <h3 v-if="status" style="text-align:center;color:#3E5C6B;">
                人不能两次登入同一个账号<br />
                你或许可以到<router-link to="/user/0/" style="color:#FF8533;text-decoration: none;">用户中心</router-link>康康
            </h3>
            <n-tabs v-else class="card-tabs" size="large" animated pane-style="box-sizing: border-box;">
                <n-tab-pane name="登录" style="padding: 4px;">
                    <n-form ref="form_ref" :rules="rules" :model="user">
                        <n-form-item path="sid" label="学号">
                            <n-input v-model:value="user.sid" type="number" placeholder="请输入BIT学号" />
                        </n-form-item>

                        <n-form-item path="password" label="密码">
                            <n-input v-model:value="user.password" type="password" show-password-on="click"
                                placeholder="告诉我你的秘密" />
                        </n-form-item>

                        <n-button @click="Login" block>登录</n-button>
                    </n-form>
                </n-tab-pane>

                <n-tab-pane name="注册或重置" style="padding: 4px;">
                    <n-alert title="Tips" :show-icon="false" :closable="true" type="info" style="margin-bottom: 11px;">
                        <p style="font-size: 11px;color: grey;">1. BITself奉行「前端匿名」理念，不会主动公开任何个人信息，你在登录后可以设置供展示的头像、昵称等。
                        </p>
                        <p style="font-size: 11px;color: grey;">2. 密码将被不可逆加密后传输到服务器。</p>
                        <p style="font-size: 11px;color: grey;">3. 你需要选择统一身份认证或学校邮箱以证明自己的身份。</p>
                    </n-alert>

                    <n-form ref="form_ref" :rules="rules" :model="user">
                        <n-form-item path="sid" label="学号">
                            <n-input v-model:value="user.sid" type="number" placeholder="请输入BIT学号" />
                        </n-form-item>

                        <n-form-item path="password" label="设置密码">
                            <n-input v-model:value="user.password" type="password" show-password-on="click"
                                placeholder="告诉我你的秘密" />
                        </n-form-item>

                        <n-form-item path="repassword" label="再次输入密码">
                            <n-input v-model:value="user.repassword" :disabled="!user.password" type="password"
                                show-password-on="click" placeholder="再次告诉我你的秘密" />
                        </n-form-item>

                        <n-form-item label="验证方式">
                            <n-radio-group v-model:value="user.verify_type">
                                <n-radio-button value="webvpn">
                                    统一身份认证
                                </n-radio-button>
                                <n-radio-button value="mail">
                                    @bit.edu.cn邮箱
                                </n-radio-button>

                            </n-radio-group>
                        </n-form-item>


                        <template v-if="user.verify_type == 'webvpn'">
                            <n-grid cols="12">
                                <n-form-item-gi span="8" :show-label="false">
                                    <n-input v-model:value="user.webvpn_password" type="password"
                                        show-password-on="click" placeholder="学校统一身份认证密码" />
                                </n-form-item-gi>
                                <n-gi span="4">
                                    <n-button @click="WebvpnVerify(user.sid,user.webvpn_password)" :disabled="!user.webvpn_password || !user.sid"
                                        :loading="webvpn.loading" block>验证</n-button>
                                </n-gi>
                            </n-grid>
                        </template>
                        <template v-else>
                            <n-grid cols="12">
                                <n-form-item-gi path="verify_code" span="8" :show-label="false">
                                    <n-input v-model:value="user.verify_code" type="number" placeholder="收到的验证码" />
                                </n-form-item-gi>
                                <n-gi span="4">
                                    <n-button @click="MailVerify" :disabled="(!user.sid) || (count_down ? true : false)"
                                        block>{{ count_down ? count_down : '发送验证码' }}</n-button>
                                </n-gi>
                            </n-grid>
                        </template>



                        <n-button @click="Register" :disabled="!user.verify_code" block>注册</n-button>
                    </n-form>
                </n-tab-pane>
            </n-tabs>
        </n-card>
        <br />
    </div>

</template>


