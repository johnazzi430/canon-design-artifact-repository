import axios from 'axios'
import api from '../api'

const actions = {
  ADlogin ({ commit }, user) {
    return new Promise((resolve, reject) => {
      user.username = user.userName

      commit('AUTH_REQUEST')
      axios({
        method: 'post',
        url: '/api/AD-login',
        data: user,
        header: {
          'Content-Type': 'application/json'
        }
      })
        .then(function (resp) {
          var token = resp.data.token

          localStorage.setItem('token', token)
          axios.defaults.headers.common.Authorization = token
          commit({
            type: 'AUTH_SUCCESS',
            token: token,
            user: user
          })
          resolve(resp)
        })
        .catch(err => {
          commit('AUTH_ERROR')
          localStorage.removeItem('token')
          reject(err)
        })
    })
  },

  login ({ commit }, user) {
    return new Promise((resolve, reject) => {
      commit('AUTH_REQUEST')
      axios({
        method: 'post',
        url: '/api/login',
        data: user,
        header: {
          'Content-Type': 'application/json'
        }
      })
        .then(function (resp) {
          var token = resp.data.token
          var user = resp.data.user

          localStorage.setItem('token', token)
          axios.defaults.headers.common.Authorization = token
          commit({
            type: 'AUTH_SUCCESS',
            token: token,
            user: user
          })
          resolve(resp)
        })
        .catch(err => {
          commit('AUTH_ERROR')
          localStorage.removeItem('token')
          reject(err)
        })
    })
    context.dispatch('getPlaylist')
    context.dispatch('getProductOptions')
    context.dispatch('getPersonaRoleOptions')
    context.dispatch('getPersonaOptions')
  },

  async enter (context) {
    context.commit('AUTH_REQUEST')
    const { data } = await api.userLoggedIn()

    context.commit({
      type: 'AUTH_SUCCESS',
      token: localStorage.getItem('token') || '',
      user: data[0]
    })

    context.dispatch('getPlaylist')
    context.dispatch('getProductOptions')
    context.dispatch('getPersonaRoleOptions')
    context.dispatch('getPersonaOptions')
  },

  logout ({ commit }) {
    return new Promise((resolve, reject) => {
      commit('logout')
      localStorage.removeItem('token')
      delete axios.defaults.headers.common.Authorization
    })
  },

  async getPlaylist (context) {
    const data = await api.getPlaylistByUser()
    context.commit('GET_PLAYLIST', data)
  },

  async getProductOptions (context) {
    const data = await api.getProductOptions()
    context.commit('GET_PRODUCT_OPTIONS', data)
  },

  async getPersonaRoleOptions (context) {
    const data = await api.getPersonaRoleOptions()
    context.commit('GET_PERSONA_ROLE_OPTIONS', data)
  },

  async getPersonaOptions (context) {
    const data = await api.getPersonaOptions()
    context.commit('GET_PERSONA_OPTIONS', data)
  }

}

export default actions
