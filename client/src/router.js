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
import About from './components/About.vue';
import Playlist from './components/Playlist.vue'
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
      beforeEnter: (to,from,next) => {
        if (store.state.role === 'admin') next()
        else next(false)
      }
    },
    {
      path: '/persona',
      name: 'persona default',
      component: PersonaPage,
      children:[
        {
          path: ':id',
          component: PersonaPage
        }
      ]
    },
    {
      path: '/product',
      name: 'product default',
      component: ProductPage,
      children:[
        {
          path: ':id',
          component: ProductPage
        }
      ]
    },
    {
      path: '/insight',
      name: 'insight default',
      component: InsightsPage,
      children:[
        {
          path: ':id',
          component: InsightsPage,
        }
      ]
    },
    {
      path: '/playlist',
      name: 'playlist',
      component: Playlist,
    },
    {
      path: '/about',
      name: 'about',
      component: About,
    },
  ],
});

router.beforeEach((to, from, next) => {
  if(to.name === "login") {
    store.state.auth_success===false
    next()
    return
  }
  else {
    if(store.getters.isLoggedIn) {
      next()
      return
    }
    else {
      next('/login')
    }
  }
})

export default router
