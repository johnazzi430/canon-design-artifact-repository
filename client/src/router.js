/*eslint-disable */
import Vue from 'vue';
import Router from 'vue-router';
//import BootstrapVue from 'bootstrap-vue';
import PersonaPage from './components/PersonaPage.vue';
import CardView from './components/Personas/CardView.vue';
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
      name: 'PersonaPage',
      component: PersonaPage,
    },
    {
      path: '/personas/cards',
      name: 'persona_cards',
      component: CardView,
    },
    {
      path: '/personas/:id',
      name: 'persona_detail',
      component: CardView,
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
