/*
 * @Author: flwfdd
 * @Date: 2022-02-20 22:45:07
 * @LastEditTime: 2022-02-21 23:31:13
 * @Description: 
 * _(:з」∠)_
 */
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import axios from 'axios'

Vue.config.productionTip = false
Vue.prototype.$axios = axios
axios.defaults.headers.common['fake_cookie'] = store.getters.get_cookie

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
