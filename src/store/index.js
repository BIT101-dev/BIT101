/*
 * @Author: flwfdd
 * @Date: 2022-02-20 22:45:07
 * @LastEditTime: 2022-02-21 23:27:11
 * @Description: 
 * _(:з」∠)_
 */
import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    base_url: "https://1426531544223608.cn-beijing.fc.aliyuncs.com/2016-08-15/proxy/bitself.LATEST/relay",
    cookie: "show_vpn=0; wengine_vpn_ticketwebvpn_bit_edu_cn=4e2286b25353b01c; refresh=0",
  },
  getters: {
    get_cookie(state) {
      state.cookie = (localStorage.getItem('cookie') || "");
      return state.cookie;
    }
  },
  mutations: {
    set_cookie(state, s) {
      axios.defaults.headers.common['fake_cookie'] = s;
      state.cookie = s;
      localStorage.setItem('cookie', s);
    }
  },
  actions: {
  },
  modules: {
  }
})
