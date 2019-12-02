/*eslint-disable */
import Vue from 'vue';
import Router from 'vue-router';
//import BootstrapVue from 'bootstrap-vue';
import PersonaPage from './components/PersonaPage.vue';
import ProductPage from './components/ProductPage.vue';
import Login from './components/Login.vue';
import NotFound from './components/NotFound.vue';
import Table from './components/Personas/Table.vue';
import CardView from './components/Personas/CardView.vue';

Vue.use(Router);
//Vue.use(BootstrapVue)

export default new Router({
  // mode: 'history',
  // base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      redirect: {
        name: 'login'
      }
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    // {
    //   path: '*',
    //   name: 'invalid',
    //   component: NotFound,
    // },
    {
      path: '/persona',
      name: 'persona default',
      component: PersonaPage,
    },
    {
      path: '/product',
      name: 'product default',
      component: ProductPage,
    },
    // {
    //   path: '/persona/cards',
    //   name: 'persona cards',
    //   component: CardView,
    // },
    // {
    //   path: '/persona/table',
    //   name: 'persona table',
    //   component: Table,
    // }
  ],
});
