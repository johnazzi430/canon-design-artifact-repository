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
    user : {
      username: '',
      role: null
    },
    alert: [],
  },
  mutations: {

    auth_request(state){
      state.status = 'loading'
    },

    auth_success(state,payload){
      state.status = 'success'
      state.token = payload.token
      state.user = payload.user
    },

    auth_error(state){
      state.status = 'error'
    },

    logout(state){
      state.status = ''
      state.token = null
      state.user = {
        username: '',
        role: null
      }
    },

    alert(state,payload){
      state.alert.push({
                time : Date.now(),
                show : payload.show,
                variant : payload.variant,
                content : payload.content
              })
    },

  },
  actions: {


    ADlogin({commit}, user){
      return new Promise((resolve, reject) => {
        user.username = user.userName;

        commit('auth_request')
        axios({
            method: 'post',
            url: '/api/AD-login',
            data: user,
            header: {
              "Content-Type":"application/json"
            }
          })
        .then(function (resp) {

          var token = resp.data.token;

          localStorage.setItem('token', token)
          axios.defaults.headers.common['Authorization'] = token
          commit({
            type: 'auth_success',
            token : token,
            user : user,
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
          var user = resp.data.user;

          localStorage.setItem('token', token)
          axios.defaults.headers.common['Authorization'] = token
          commit({
            type: 'auth_success',
            token : token,
            user : user,
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

    async enter(context) {
      axios({
          method : 'get',
          url : `/api/users`,
          params : {
            'session' : 'true'
          }
        })
        .then(response => {
          context.commit({
            type: 'auth_success',
            token : localStorage.getItem('token') || '',
            user : response.data[0],
          })
          return true;
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
    user: state => state.user,
    alert: state => state.alert,
  },
});
