/*
 * @Author: flwfdd
 * @Date: 2022-02-20 22:45:07
 * @LastEditTime: 2022-03-14 00:01:42
 * @Description: 
 * _(:з」∠)_
 */
import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    api_url: "http://bitself.flwfdd.xyz:5555",
    fake_cookie:"",
    webvpn_cookie: "",
    webvpn_username:"",
    webvpn_password:"",
  },
  mutations: {
    set_fake_cookie(state, s) {
      axios.defaults.headers.common['fake_cookie'] = s;
      state.fake_cookie = s;
    },
    set_webvpn_cookie(state, s) {
      state.webvpn_cookie = s;
    },
    set_webvpn_login(state,payload){
      state.webvpn_username=payload.username;
      state.webvpn_password=payload.password;
    }
  },
  actions: {
  },
  modules: {
  },
  plugins: [createPersistedState({
    reducer(val){
      return {
        fake_cookie:val.fake_cookie,
        webvpn_cookie:val.webvpn_cookie,
        webvpn_username:val.webvpn_username,
        webvpn_password:val.webvpn_password
      }
    }
  })],
})
