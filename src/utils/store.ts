/*
 * @Author: flwfdd
 * @Date: 2022-05-28 09:18:09
 * @LastEditTime: 2023-05-16 12:21:29
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
  img_suffix: "!low",
  fake_cookie: String(x.fake_cookie) || "Here's fake_cookie",
  // 缓存成绩查询的学号
  grade_query_sid: String(x.grade_query_sid) || "",
  // 缓存成绩查询的类型和时间
  grade_query_course_type_filter: (x.grade_query_course_type_filter as string[]) || [],
  grade_query_course_time_filter: (x.grade_query_course_time_filter as string[]) || [],
})

watch(store, () => {
  window.localStorage.setItem('store', JSON.stringify(store));
})

// console.log(store);

export default store