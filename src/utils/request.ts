/*
 * @Author: flwfdd
 * @Date: 2022-05-28 08:34:05
 * @LastEditTime: 2022-07-10 20:19:11
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
    return config;
  },
  (err) => {
    return Promise.reject(err);
  }
);

// 添加响应拦截器
http.interceptors.response.use(
  (res) => {
    if (res.data.msg) window.$message.success(res.data.msg);
    return res;
  },
  (err) => {
    if (err.request.status == 500) {
      if (err.response.data.msg) window.$message.error(err.response.data.msg);
      else window.$message.error('出错了Orz');
    }
    else if (err.request.status == 401) {
      // 如果当前已经处于登录页面，什么也不做
      const route = router.currentRoute.value;
      console.log("currentRoute", route);
      if (route.name != "login") {
        window.$message.error(err.response.data.msg || '请先登录awa');
      }
    }
    else if (err.request.status == 400) {
      if (err.response.data.msg) window.$message.error(err.response.data.msg);
      else window.$message.error('请检查请求参数awa');
    }
    return Promise.reject(err);
  }
);

export default http;