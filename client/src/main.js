/*eslint-disable */
import Vue from 'vue';
import App from './App.vue';
import BootstrapVue from 'bootstrap-vue';
import Multiselect from 'vue-multiselect';
import Axios from 'axios';
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

Vue.component('multiselect', Multiselect)

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

router.start(App, '#Entry');
