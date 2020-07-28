
const getters = {
  isLoggedIn: state => { return !!state.token },
  authStatus: state => { return state.status },
  user: state => state.user,
  alert: state => state.alert,
  isItemOnPlaylist: (state) => (table, id) => {
    return state.playlist.find(item => item.source_id === id && item.source_table === table)
  }
}

export default getters
