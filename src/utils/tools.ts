/*
 * @Author: flwfdd
 * @Date: 2022-05-28 00:01:07
 * @LastEditTime: 2025-05-12 21:00:02
 * @Description: 一些全局使用的函数
 * _(:з」∠)_
 */
import { ref, reactive } from "vue";
import http from "@/utils/request";
import { encryptPassword } from "./EncryptPassword";
import useClipboard from "vue-clipboard3";
import router from "@/router";
import store from "@/utils/store";

//一言
const hitokoto = ref("");
function UpHitokoto() {
  http.get("https://international.v1.hitokoto.cn/").then((res) => {
    hitokoto.value = res.data.hitokoto + "  ——" + res.data.from;
  });
}

UpHitokoto();
setInterval(UpHitokoto, 10 * 1000);

//时间格式化
function FormatTime(t: number | Date | string) {
  if (!t) return "No Time";
  if (typeof t == "string") {
    //日期以GMT结尾时使用本地时区
    if (t.endsWith("GMT")) t = t.replace("GMT", "");
    t = new Date(t);
    t = t.getTime() / 1000;
  } else if (typeof t != "number") t = t.getTime() / 1000;
  let dt = new Date().getTime() / 1000 - t;
  if (dt < 60) return Math.round(dt) + "秒前";
  if (dt < 60 * 60) return Math.round(dt / 60) + "分钟前";
  if (dt < 12 * 60 * 60) return Math.round(dt / 60 / 60) + "小时前";

  let now = new Date(t * 1000);
  let year = now.getFullYear();
  let month = (now.getMonth() + 1).toString().padStart(2, "0");
  let date = now.getDate().toString().padStart(2, "0");
  let hour = now.getHours().toString().padStart(2, "0");
  let minute = now.getMinutes().toString().padStart(2, "0");
  let second = now.getSeconds().toString().padStart(2, "0");
  return (
    year + "-" + month + "-" + date + " " + hour + ":" + minute + ":" + second
  );
}

//Webvpn模块
const webvpn = reactive({
  sid: "",
  password: "",
  jwb_cookie: "",
  jxzxehall_cookie: "",
  loading: false
});

function GetWebVPNJWBCookie(sid: string, password: string) {
  webvpn.loading = true;
  return http
    .post(`${store.bit_login_url}/api/jwb/cookies`, {
      username: sid,
      password: password,
    })
    .then((res) => {
      const responseData = res.data || res;
      webvpn.jwb_cookie = responseData.cookie_str;
      webvpn.loading = false;
      if (webvpn.jwb_cookie) {
        window.$message?.success("获取教务部 Cookies 成功OvO");
      } else {
        window.$message?.error(`获取教务部 Cookies 失败: 空的返回值`);
      }
      return webvpn.jwb_cookie;
    })
    .catch((err) => {
      webvpn.loading = false;
      const errorMsg = err.response?.data?.detail || err.message || "未知错误";
      window.$message?.error(`获取教务部 Cookies 失败: ${errorMsg}`);
      console.error(err);
      return Promise.reject(err);
    });
}

function GetWebVPNJXZXEHALLCookie(sid: string, password: string) {
  webvpn.loading = true;
  return http
    .post(`${store.bit_login_url}/api/jxzxehall/cookies`, {
      username: sid,
      password: password,
    })
    .then((res) => {
      const responseData = res.data || res;
      webvpn.jxzxehall_cookie = responseData.cookie_str;
      webvpn.loading = false;
      if (webvpn.jxzxehall_cookie) {
        window.$message?.success("获取教学中心 Cookies 成功OvO");
      } else {
        window.$message?.error(`获取教学中心 Cookies 失败: 空的返回值`);
      }
      return webvpn.jxzxehall_cookie;
    })
    .catch((err) => {
      webvpn.loading = false;
      const errorMsg = err.response?.data?.detail || err.message || "未知错误";
      window.$message?.error(`获取教学中心 Cookies 失败: ${errorMsg}`);
      console.error(err);
      return Promise.reject(err);
    });
}


//复制
const { toClipboard } = useClipboard();
async function Clip(s: string, msg = "已复制到剪贴板OvO") {
  try {
    await toClipboard(s);
    window.$message.success(msg);
  } catch (e) {
    console.error(e);
    window.$message.error("复制失败Orz");
  }
}

// 分享
export function Share(title: string, text: string, url: string) {
  if (navigator.share) {
    navigator
      .share({
        title: title,
        text: text,
        url: url,
      })
      .then(() => {
        window.$message.success("分享成功OvO");
      })
      .catch(() => {
        window.$message.error("分享失败Orz");
      });
  } else {
    Clip(url, "分享链接已复制OvO");
  }
}

// 打开链接
export function OpenLink(url: string, blank = false) {
  if (url) {
    if (url.startsWith("/") && blank == false) router.push(url);
    else
      window.open(
        url,
        blank ? "_blank" : url.startsWith("/") ? "_self" : "_blank"
      );
  }
}

// 监测网络情况
const network = ref(true);
export function WatchNetwork() {
  window.addEventListener("offline", () => {
    if (network.value == true) window.$message.error("网络已断开Orz");
    network.value = false;
  });

  window.addEventListener("online", () => {
    if (network.value == false) window.$message.success("网络已连接OvO");
    network.value = true;
  });
}

/** 设置页面标题 */
export function setTitle(...titles: string[]): void {
  if (titles.length === 0) {
    document.title = "BIT101";
    return;
  }
  document.title = `${titles.join(" - ")} | BIT101`;
}

// 设置颜色透明度
export function opacityColor(color: string, opacity: number): string {
  if (color.startsWith("#")) {
    let r = parseInt(color.slice(1, 2), 16);
    r = r * 16 + r;
    let g = parseInt(color.slice(2, 3), 16);
    g = g * 16 + g;
    let b = parseInt(color.slice(3, 4), 16);
    b = b * 16 + b;
    if (color.length > 5) {
      r = parseInt(color.slice(1, 3), 16);
      g = parseInt(color.slice(3, 5), 16);
      b = parseInt(color.slice(5, 7), 16);
    }
    color = `rgba(${r}, ${g}, ${b}, ${opacity})`;
  } else if (color.startsWith("rgb")) {
    color = color.replace("rgb", "rgba").replace(")", `, ${opacity})`);
  } else if (color.startsWith("rgba")) {
    color = color.replace(/,\s*[\d.]+\)/, `, ${opacity})`);
  }
  return color;
}


function GetObjName(obj: string) {
  if (obj.startsWith("like")) return "赞";
  if (obj.startsWith("poster")) return "帖子";
  if (obj.startsWith("comment")) return "评论";
  if (obj.startsWith("course")) return "课程";
  if (obj.startsWith("paper")) return "文章";
  return "";
}

function GetObjUrl(obj: string) {
  if (obj.startsWith("paper")) return "/paper/" + obj.substring(5);
  if (obj.startsWith("course")) return "/course/" + obj.substring(6);
  if (obj.startsWith("poster")) return "/gallery/" + obj.substring(6);
  return "";
}

export { hitokoto, FormatTime, webvpn, GetWebVPNJWBCookie, GetWebVPNJXZXEHALLCookie, Clip, GetObjName, GetObjUrl };
