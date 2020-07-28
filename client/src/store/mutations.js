
const mutations = {

  AUTH_REQUEST (state) {
    state.status = 'loading'
  },

  AUTH_SUCCESS (state, payload) {
    state.status = 'success'
    state.token = payload.token
    state.user = payload.user
  },

  AUTH_ERROR (state) {
    state.status = 'error'
  },

  LOGOUT (state) {
    state.status = ''
    state.token = null
    state.user = {
      username: '',
      role: null
    }
  },

  alert (state, payload) {
    state.alert.push({
      time: Date.now(),
      show: payload.show,
      variant: payload.variant,
      content: payload.content
    })
  },

  GET_PLAYLIST (state, payload) {
    state.playlist = payload.data
  },

  GET_PRODUCT_OPTIONS (state, payload) {
    state.products = payload.data
  },

  GET_PERSONA_ROLE_OPTIONS (state, payload) {
    state.persona_roles = payload.data
  },

  GET_PERSONA_OPTIONS (state, payload) {
    state.personas = payload.data
  }
}

export default mutations
