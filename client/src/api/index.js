

import axios from 'axios'

const API_URL = process.env.API_URL

export function getPersona () {
  return axios.get(`${API_URL}/persona-table`)
}
