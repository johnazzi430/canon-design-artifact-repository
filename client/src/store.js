/*eslint-disable */
import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

import { isValidJwt, EventBus } from './index.js';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user : {},
    role : null
  },
  mutations: {

    auth_request(state){
      state.status = 'loading'
    },

    auth_success(state,payload){
      state.status = 'success'
      state.token = payload.token
      state.user = payload.user
      state.role = payload.role
    },

    auth_error(state){
      state.status = 'error'
    },

    logout(state){
      state.status = ''
      state.token = null
      state.role = ''
    }

  },
  actions: {

    login({commit}, user){
      return new Promise((resolve, reject) => {

        commit('auth_request')
        axios({
            method: 'post',
            url: '/api/login',
            data: user,
            header: {
              "Content-Type":"application/json"
            }
          })
        .then(function (resp) {

          var token = resp.data.token;
          var user = resp.data.username;
          var role = resp.data.role;
          console.log(resp.data.role)
          localStorage.setItem('token', token)
          axios.defaults.headers.common['Authorization'] = token
          commit({
            type: 'auth_success',
            token : token,
            user : user,
            role : role
          })
          resolve(resp)
        })
        .catch(err => {
          commit('auth_error')
          localStorage.removeItem('token')
          reject(err)
        })
      })
    },

    logout({commit}){
      return new Promise((resolve, reject) =>{
        commit('logout')
        localStorage.removeItem('token')
        delete axios.defaults.headers.common['Authorization']
      })
    },

  },
  getters : {
    isLoggedIn: state => {return !!state.token},
    authStatus: state => {return state.status},
    userRole: state => {return state.role},
  },
});
