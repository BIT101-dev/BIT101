/*
 * @Author: flwfdd
 * @Date: 2022-05-28 09:18:09
 * @LastEditTime: 2022-07-06 00:00:15
 * @Description: 全局状态管理
 * _(:з」∠)_
 */
import { reactive, watch } from 'vue'
import package_json from '../../package.json'

let s = window.localStorage.getItem('store');
let x:any={};
if(s)x=JSON.parse(s);
else x={};

const store = reactive({
    version: package_json.version,
    api_url: "http://172.29.4.192:5000",
    fake_cookie: x.fake_cookie||"Here's fake_cookie",
})

watch(store, () => {
    window.localStorage.setItem('store', JSON.stringify(store));
})

// console.log(store);

export default store