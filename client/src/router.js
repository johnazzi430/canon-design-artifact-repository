/*eslint-disable */
import Vue from 'vue';
import Router from 'vue-router';
//import BootstrapVue from 'bootstrap-vue';
import PersonaPage from './components/PersonaPage.vue';
import ProductPage from './components/ProductPage.vue';
import InsightsPage from './components/InsightsPage.vue';
import Admin from './components/Admin.vue';
import Login from './components/Login.vue';
import NotFound from './components/NotFound.vue';
import Home from './components/Home.vue';
import {EventBus} from  "./index.js";
import store from  "./store";

Vue.use(Router);


const router =  new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/admin',
      name: 'admin',
      component: Admin,
    },
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
    {
      path: '/insights',
      name: 'insights default',
      component: InsightsPage,
    },
  ],
});
// 
// router.beforeEach((to, from, next) => {
//   if(to.name === "login") {
//     store.state.authenticated===false
//     next()
//     return
//   }
//   else {
//     if(store.state.authenticated === true && store.state.role != null) {
//       next()
//       return
//     }
//     else {
//       next('/login')
//     }
//   }
// })

export default router
