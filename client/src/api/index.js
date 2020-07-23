

import axios from 'axios';

const { API_URL } = process.env;

export default {

  //UserManagement
  userLoggedIn() {
    const  params = {  'session' : 'true'}
    return axios.get(`/api/users`,{params : params});
  },

  logIn() {
    const  params = {  'session' : 'true'}
    return axios.get(`/api/users`,{params : params});
  },


  // PERSONAS
  personaTable() {
    return axios.get(`/api/persona`);
  },

  getPersonaOptions() {
    return axios.get(`/api/personas`);
  },

  personaPost(data) {
    return axios.post(`/api/persona`, data);
  },

  personaTableById(id) {
    return axios.get(`/api/persona/${id}`);
  },

  personaFilesById(id) {
    return axios.get(`/api/persona/files/${id}`);
  },

  personaTablePutById(id, data) {
    return axios.put(`/api/persona/${id}`, data);
  },

  putPersonaAvatar(id,data) {
    var formData = new FormData();
    formData.append('file', this.$refs.pictureInput.file);
    return axios.post(`/api/persona/files/${id}`,formData,{headers: {'Content-Type': 'multipart/form-data'}});
  },

  putPersonaFilesById(id,data) {
    var formData = new FormData();
    var mime = require('mime-types')

    formData.append('file', data);
    formData.append('filename', 'blank');
    return axios.post(`/api/persona/files/${id}`,formData,{headers: {'Content-Type': 'multipart/form-data'}});
  },

  deletePersonaFilesById(id,data) {
    return axios.delete(`/api/persona/files/${id}`);
  },

  getPersonaRoleOptions(){
    return axios.get("/api/persona/roles");
  },

  // PRODUCTS
  productTable() {
    return axios.get("/api/product");
  },

  getProductOptions() {
    return axios.get("/api/products");
  },

  productPost(data) {
    return axios.post(`/api/products`, data);
  },

  productTableById(id) {
    return axios.get(`/api/product/${id}`);
  },

  productTablePutById(id, data) {
    return axios.put(`${API_URL}/product/${id}`, data);
  },

  productFilesById(id) {
    return axios.get(`/api/product/files/${id}`);
  },

  putProductFilesById(id,data) {
    var formData = new FormData();
    var mime = require('mime-types')

    formData.append('file', data);
    formData.append('filename', 'blank');
    return axios.post(`/api/product/files/${id}`,formData,{headers: {'Content-Type': 'multipart/form-data'}});
  },

  deleteProductFilesById(id,data) {
    return axios.delete(`/api/product/files/${id}`);
  },

  // INSIGHTS
  insightTable() {
    return axios.get(`api/insights`);
  },

  insightPost(data) {
    return axios.post(`/api/insights`, data);
  },

  insightTableById(id) {
    return axios.get(`/api/insights/${id}`);
  },

  insightTablePutById(id, data) {
    return axios.put(`/api/insights/${id}`, data);
  },

  insightFilesById(id) {
    return axios.get(`/api/insights/files/${id}`);
  },

  putinsightFilesById(id,data) {
    var formData = new FormData();
    var mime = require('mime-types')

    formData.append('file', data);
    formData.append('filename', 'blank');
    return axios.post(`/api/insights/files/${id}`,formData,{headers: {'Content-Type': 'multipart/form-data'}});
  },

  deleteinsightFilesById(id,data) {
    return axios.delete(`/api/insights/files/${id}`);
  },


  // COMMENTS
  async getItemComments(source_table,id){
    return await axios.get(`/api/${source_table}/comments/${id}`)
  },

  async addComment(source_table,id,data){
    return await axios.post(`/api/${source_table}/comments/${id}`,data)
  },

  // Playlist
  getPlaylistByUser() {
    return axios.get(`/api/playlist`)
  },

  async getPlaylistDetails() {
    return await axios.get(`/api/playlist?details=True`)
  },

  async addToPlaylist(params) {
    await axios.post('/api/playlist', params)
  },

  async removeFromPlaylist(params) {
    await axios.post('/api/playlist/delete', params)
  },


  // Admin
  getUsers(params) {
    return axios.get('/api/users')
  },

  editUserInfo(id,data) {
    return axios.put(`/api/users/${id}`,data)
  },

  resetUserPassword(id) {
    return axios.put(`/api/users/${id}/password-reset`)
  },


};
