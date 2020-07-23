/*eslint-disable */
import Vue from 'vue';
import App from './App.vue';
import BootstrapVue from 'bootstrap-vue';
import Multiselect from 'vue-multiselect';
import VueDraggable from 'vue-draggable'
import PlaylistAdd from './components/Playlist/PlaylistAdd.vue'
import Axios from 'axios';
import moment from 'moment'
import router from './router';
import store from './store/index';

// CSS
import '@ag-grid-community/all-modules/dist/styles/ag-grid.css';
import '@ag-grid-community/all-modules/dist/styles/ag-theme-balham.css';
import "@ag-grid-community/all-modules/dist/styles/ag-theme-material.css";
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap-vue/dist/bootstrap-vue.css"
import "./styles.css";
import '@fortawesome/fontawesome-free/css/all.css'
import '@fortawesome/fontawesome-free/js/all.js'
import { fas } from '@fortawesome/free-solid-svg-icons'


Vue.config.productionTip = false;

Vue.use(BootstrapVue)
Vue.use(VueDraggable)
Vue.component('multiselect', Multiselect)
Vue.component('playlist-add', PlaylistAdd)


Vue.prototype.$http = Axios;
const token = localStorage.getItem('token')
if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = token;
}

Vue.component('multiselect', Multiselect)

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app');

Vue.filter('capitalize', function (value) {
  if (!value) return ''
  value = value.toString()
  return value.charAt(0).toUpperCase() + value.slice(1)
})

Vue.filter('formatDate', function(value) {
  if (value) {
    return moment.utc(value).fromNow()
  }
})
