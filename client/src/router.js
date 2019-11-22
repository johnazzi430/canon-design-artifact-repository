import Vue from 'vue';
import Router from 'vue-router';
import Table from './components/Table.vue';


Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Table',
      component: Table,
    },

  ],
});
