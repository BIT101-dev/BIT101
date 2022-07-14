/*
 * @Author: flwfdd
 * @Date: 2022-05-28 00:01:07
 * @LastEditTime: 2022-07-13 00:13:52
 * @Description: 一些全局使用的函数
 * _(:з」∠)_
 */
import { ref, reactive } from 'vue'
import http from '@/utils/request';
import { encryptPassword } from './EncryptPassword';
import useClipboard from 'vue-clipboard3'

//一言
const hitokoto = ref("")
function UpHitokoto() {
  http.get("https://v1.hitokoto.cn/")
    .then((res) => {
      hitokoto.value = res.data.hitokoto + "  ——" + res.data.from;
    })
}

UpHitokoto();
setInterval(UpHitokoto, 10 * 1000);

//时间格式化
function FormatTime(t: number | Date | string) {
  if (!t) return "No Time";
  if (typeof (t) == 'string') { //日期以GMT结尾时使用本地时区
    if (t.endsWith('GMT')) t = t.replace('GMT', '');
    t = new Date(t);
    t = t.getTime() / 1000;
  }
  else if (typeof (t) != 'number') t = t.getTime() / 1000;
  let dt = new Date().getTime() / 1000 - t;
  if (dt < 60) return Math.round(dt) + "秒前";
  if (dt < 60 * 60) return Math.round(dt / 60) + "分钟前";
  if (dt < 12 * 60 * 60) return Math.round(dt / 60 / 60) + "小时前"

  let now = new Date(t * 1000);
  let year = now.getFullYear();
  let month = now.getMonth() + 1;
  let date = now.getDate();
  let hour = now.getHours();
  let minute = now.getMinutes();
  let second = now.getSeconds();
  return year + "-" + month + "-" + date + " " + hour + ":" + minute + ":" + second;
}

//Webvpn模块
const webvpn = reactive({
  model: false,
  loading: false,
  sid: "",
  password: "",
  verify_code: "",
  cookie: "",
  data: {
    execution: "",
    cookie: "",
    salt: "",
    captcha: "",
    captcha_text: "",
    password: ""
  }
})

//webvpn验证初始化
function WebvpnVerify(sid: string, password: string) {
  webvpn.loading = true;
  webvpn.sid = sid;
  webvpn.password = password;
  http.get("/user/webvpn_verify_init/?sid=" + webvpn.sid)
    .then((res) => {
      webvpn.data = res.data;
      webvpn.data.password = encryptPassword(webvpn.password, webvpn.data.salt);
      if (webvpn.data.captcha) {
        webvpn.data.captcha = "data:image/png;base64," + webvpn.data.captcha;
        webvpn.data.captcha_text = "";
        webvpn.model = true;
      }
      else WebvpnVerify2();
    })
}

//webvpn验证后续步骤
function WebvpnVerify2() {
  webvpn.model = false;
  http.post("/user/webvpn_verify/", {
    username: webvpn.sid,
    password: webvpn.data.password,
    execution: webvpn.data.execution,
    cookie: webvpn.data.cookie,
    captcha: webvpn.data.captcha_text
  })
    .then((res) => {
      webvpn.verify_code = res.data.verify_code;
      webvpn.cookie = res.data.cookie;
      webvpn.loading = false;
    })
    .catch(() => {
      webvpn.loading = false;
    });
}

//复制
const {toClipboard}=useClipboard();
async function Clip(s:string,msg="已复制到剪贴板OvO"){
  try {
    await toClipboard(s)
    window.$message.success(msg);
  } catch (e) {
    console.error(e)
    window.$message.error("复制失败Orz");
  }
}

export {
  hitokoto,
  FormatTime,
  webvpn,
  WebvpnVerify,
  WebvpnVerify2,
  Clip,
}