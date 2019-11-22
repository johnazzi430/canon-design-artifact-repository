/*eslint-disable */
import Vue from 'vue';
import Router from 'vue-router';
//import BootstrapVue from 'bootstrap-vue';
import Table from './components/Table.vue';
import Ping from './components/Ping.vue';
import InputForm from './components/InputForm.vue';



Vue.use(Router);
//Vue.use(BootstrapVue)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [

    {
      path: '/',
      name: 'table',
      component: Table,
    },
    {
      path: '/add_data',
      name: 'add_data',
      component: InputForm,
    },

  ],
});
