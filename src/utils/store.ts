/*
 * @Author: flwfdd
 * @Date: 2022-05-28 09:18:09
 * @LastEditTime: 2023-11-01 22:50:07
 * @Description: 全局状态管理
 * _(:з」∠)_
 */
import { reactive, watch } from 'vue'
import package_json from '../../package.json'

let s = window.localStorage.getItem('store');
let x: any = {};
if (s) x = JSON.parse(s);
else x = {};

const store = reactive({
  version: package_json.version,
  api_url: "https://bit101.flwfdd.xyz",
  // api_url: "http://127.0.0.1:8080",
  // api_url: "http://e5.flwfdd.xyz:8080",
  // api_url:"http://127.0.0.1:4523/m1/2401657-0-default",
  // api_url:"http://192.168.0.108:4523/m1/2401657-0-default",
  fake_cookie: x.fake_cookie || "",
  grade_query: x.grade_query || {},
})

watch(store, () => {
  window.localStorage.setItem('store', JSON.stringify(store));
})

// console.log(store);

export default store