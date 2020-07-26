
import Vue from 'vue';
import Vuex, { StoreOptions } from 'vuex';
import state from './state';
import getters from './getters';
import mutations from './mutations';
import actions from './actions';

Vue.use(Vuex);

export const storeOpts = {
  state,
  getters,
  mutations,
  actions,
};

const store = new Vuex.Store(storeOpts);

export default store;
