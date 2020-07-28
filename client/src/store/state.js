
const rootState = {
  status: '',
  token: localStorage.getItem('token') || '',
  user: {
    username: '',
    role: null
  },
  alert: [],
  playlist: [],
  personas: [],
  products: [],
  persona_roles: []
}

export default rootState
