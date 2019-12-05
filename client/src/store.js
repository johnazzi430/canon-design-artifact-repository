/*eslint-disable */
import Vue from 'vue';
import Vuex from 'vuex';

import { isValidJwt, EventBus } from './index.js';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    authenticated: false,
    status: '',
    token: localStorage.getItem('token') || '',
    user : {}
  },
  mutations: {
  },
  actions: {
    //
    // login({commit}, user){
    //   return new Promise((resolve, reject) => {
    //     commit('auth_request')
    //     axios({url: 'http://localhost:3000/login', data: user, method: 'POST' })
    //     .then(resp => {
    //       const token = resp.data.token
    //       const user = resp.data.user
    //       localStorage.setItem('token', token)
    //       axios.defaults.headers.common['Authorization'] = token
    //       commit('auth_success', token, user)
    //       resolve(resp)
    //     })
    //     .catch(err => {
    //       commit('auth_error')
    //       localStorage.removeItem('token')
    //       reject(err)
    //     })
    //   })
    //},

  },
  getters : {
    // isLoggedIn: state => !!state.token,
    // authStatus: state => state.status,
    //
    // isAuthenticated (state) {
    //   return isValidJwt(state.jwt.token)
    // }
  },
});
