/*eslint-disable */
import Vue from 'vue';
import Router from 'vue-router';
//import BootstrapVue from 'bootstrap-vue';
import PersonaPage from './components/Personas/PersonaPage.vue';
import ProductPage from './components/Products/ProductPage.vue';
import InsightsPage from './components/Insights/InsightsPage.vue';
import Admin from './components/UserManagement/Admin.vue';
import Login from './components/UserManagement/Login.vue';
import NotFound from './components/NotFound.vue';
import Home from './components/Home.vue';
import About from './components/About/About.vue';
import Playlist from './components/Playlist/Playlist.vue'
import {EventBus} from  "./index.js";
import store from  "./store";

Vue.use(Router);


const router =  new Router({
  mode:'history',
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
        if (store.getters.user.role === 'admin') next()
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

router.beforeEach( async (to, from, next) => {
  if(to.name === "login") {
    store.state.auth_success===false
    next()
    return
  }
  else {
    await store.dispatch('enter')
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
