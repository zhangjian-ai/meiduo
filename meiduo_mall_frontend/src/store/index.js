// import { turn } from 'core-js/core/array';
import Vue from 'vue'
import Vuex from 'vuex'


Vue.use(Vuex)

export default new Vuex.Store({
  state: {

    // 登陆信息。vuex是响应式的，当页面刷新就会感应到，会导致state中保存的值初始化。
    // 所以单纯的将登陆信息保存到state中，一旦刷新页面登陆信息就没了
    username: localStorage.username || sessionStorage.username,
    token: localStorage.token || sessionStorage.token


  },
  mutations: {
    // 登陆信息设置
    setStatus(state, payload) {
      if (payload) {
        state.token = payload.token;
        state.username = payload.username;
      } else {
        state.token = "";
        state.username = "";
        localStorage.clear();
        sessionStorage.clear();
      }
    },

  },
  actions: {

  },
  modules: {
  }
})
