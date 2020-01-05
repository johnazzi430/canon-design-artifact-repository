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
import store from './store';



// CSS
import '@ag-grid-community/all-modules/dist/styles/ag-grid.css';
import '@ag-grid-community/all-modules/dist/styles/ag-theme-balham.css';
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap-vue/dist/bootstrap-vue.css"
import "./styles.css";


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
    return moment(String(value)).fromNow()
  }
})

router.start(App, '#Entry');
