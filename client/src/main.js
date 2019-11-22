/*eslint-disable */
import Vue from 'vue';
import App from './App.vue';
import BootstrapVue from 'bootstrap-vue'
import axios from 'axios'
import router from './router';

// CSS
import '@ag-grid-community/all-modules/dist/styles/ag-grid.css';
import '@ag-grid-community/all-modules/dist/styles/ag-theme-balham.css';
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap-vue/dist/bootstrap-vue.css"

Vue.config.productionTip = false;

Vue.use(BootstrapVue)

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
