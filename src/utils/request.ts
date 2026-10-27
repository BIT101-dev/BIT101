/*
 * @Author: flwfdd
 * @Date: 2022-05-28 08:34:05
 * @LastEditTime: 2023-10-31 00:11:43
 * @Description: 
 * _(:з」∠)_
 */
import axios from 'axios';
import store from './store';
// import { useRouter, useRoute } from 'vue-router';
import router from "../router/index";

const http = axios.create();

// 添加请求拦截器
http.interceptors.request.use(
  (config: any) => {
    if (config.url[0] == '/') config.url = store.api_url + config.url;
    config.headers['fake-cookie'] = store.fake_cookie;
    if (config.url.startsWith(store.api_url + '/')) {
      config.headers['X-BIT101-Platform'] = 'web';
      config.headers['X-BIT101-Version'] = store.version;
    }
    return config;
  },
  (err) => {
    return Promise.reject(err);
  }
);

// 添加响应拦截器
http.interceptors.response.use(
  (res) => {
    if (res.data.msg&&window.$message) window.$message.success(res.data.msg);
    return res;
  },
  (err) => {
    if (err.response?.status === 409 && err.response?.data?.challenge) {
      return Promise.reject(err);
    }
    if (err.request&&err.request.status == 500) {
      if (err.response.data.msg) window.$message.error(err.response.data.msg);
      else window.$message.error("出错了Orz");
    } else if (err.request && err.request.status == 401) {
      store.fake_cookie = "";
      // 自动跳转
      const route = router.currentRoute.value;
      if (route.name != "login") {
        var msg = err.response.data.msg || err.response.data.detail || "请先登录awa";
        window.$message.error(msg);
      } else if (err.response.data.msg) {
        window.$message.error(err.response.data.msg);
      }
      if (route.meta.login) {
        router.push({
          name: "login",
          query: { redirect: encodeURIComponent(route.fullPath) },
        });
      }
    } else if (err.request && err.request.status == 400) {
      if (err.response.data.msg) window.$message.error(err.response.data.msg);
      else window.$message.error("请检查请求参数awa");
    } else if (err.request && err.request.status) {
      const status = err.request.status;
      const messages: Record<number, string> = {
        429: "学校请求并发已满，请稍后重试",
        413: "学校返回的内容过大",
        502: "学校代理暂时不可用",
        504: "学校代理响应超时",
      };
      window.$message.error(err.response?.data?.msg || messages[status] || `请求失败（HTTP ${status}）`);
      err.__bit101Notified = true;
    } else if (err.request) {
      window.$message.error("无法连接服务器，请检查网络或服务器状态");
      err.__bit101Notified = true;
    }
    return Promise.reject(err);
  }
);

export default http;