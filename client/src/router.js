/*eslint-disable */
import Vue from 'vue';
import Router from 'vue-router';
//import BootstrapVue from 'bootstrap-vue';
import PersonaData from './components/PersonaData.vue';
import Table from './components/Table.vue';
import InputForm from './components/InputForm.vue';



Vue.use(Router);
//Vue.use(BootstrapVue)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [

    {
      path: '/',
      name: 'PersonaData',
      component: PersonaData,
    },
    {
      path: '/table',
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
