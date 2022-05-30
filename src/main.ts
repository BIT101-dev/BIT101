/*
 * @Author: flwfdd
 * @Date: 2022-05-28 00:01:07
 * @LastEditTime: 2022-05-28 01:24:39
 * @Description: 
 * _(:з」∠)_
 */
import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index'

const app = createApp(App);
app.use(router)
app.mount('#app')
