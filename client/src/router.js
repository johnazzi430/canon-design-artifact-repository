/*eslint-disable */
import Vue from 'vue';
import Router from 'vue-router';
//import BootstrapVue from 'bootstrap-vue';
import PersonaPage from './components/PersonaPage.vue';
import ProductPage from './components/ProductPage.vue';
import Login from './components/Login.vue';
import NotFound from './components/NotFound.vue';
import Home from './components/Home.vue';
import {EventBus} from  "./index.js";
import store from  "./store";

Vue.use(Router);


const router =  new Router({
  // mode: 'history',
  // base: process.env.BASE_URL,


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
      path: '/persona',
      name: 'persona default',
      component: PersonaPage,
    },
    {
      path: '/product',
      name: 'product default',
      component: ProductPage,
    },
  ],
});

// router.beforeEach((to, from, next) => {
//   console.log(store.state.authenticated)
//   console.log(to)
//   if(to.name === "login") {
//     next()
//     return
//   }
//   else {
//     if(store.state.authenticated === true) {
//       next()
//       return
//     }
//     else {
//       next('/login')
//     }
//   }
// })

export default router
