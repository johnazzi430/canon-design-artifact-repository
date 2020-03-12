

import axios from 'axios';

const { API_URL } = process.env;

// PERSONAS
export function persona_table() {
  return axios.get(`${API_URL}/persona`);
}

export function persona_list() {
  return axios.get(`${API_URL}/personas`);
}

export function persona_post(data) {
  return axios.post(`${API_URL}/personas`, data);
}

export function persona_table_by_id(id) {
  return axios.get(`${API_URL}/personas/${id}`);
}

export function persona_table_put_by_id(id, data) {
  return axios.put(`${API_URL}/personas/${id}`, data);
}

// PRODUCTS
export function product_table() {
  return axios.get(`${API_URL}/product`);
}

export function product_list() {
  return axios.get(`${API_URL}/products`);
}

export function product_post(data) {
  return axios.post(`${API_URL}/products`, data);
}

export function product_table_by_id(id) {
  return axios.get(`${API_URL}/products/${id}${id}`);
}

export function product_table_put_by_id(id, data) {
  return axios.put(`${API_URL}/products/${id}`, data);
}

//
//
// @api.route("/comments/<table>/<int:id>" , methods = ['GET'])
// def comments_by_table_and_item(table,id):
//
// @api.route("/comments/<table>/<int:id>" , methods = ['POST'])
// def comments_create_by_table_and_item(table,id):
//
// @api.route("/persona-product-relationship/" , methods = ['GET'])
// def persona_product_relationship_get():
//
// @api.route("/persona-product-relationship" , methods = ['POST'])
// def persona_product_rel_post():
