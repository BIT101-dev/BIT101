/*
 * @Author: flwfdd
 * @Date: 2022-02-20 22:45:07
 * @LastEditTime: 2022-03-20 11:27:46
 * @Description: 
 * _(:з」∠)_
 */
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import axios from 'axios'
import VueClipboard from 'vue-clipboard2'

Vue.use(VueClipboard)

Vue.config.productionTip = false
Vue.prototype.$axios = axios
axios.defaults.headers.common['fake_cookie'] = store.state.fake_cookie

axios.interceptors.response.use(res=> {
  return res;
}, err=>{
  if(err.request.status==401){
    store.commit('msg','登陆失败Orz');
  }
  return Promise.reject(err);
});

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
