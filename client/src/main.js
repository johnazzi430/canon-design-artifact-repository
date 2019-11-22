/*eslint-disable */
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import Nav from './components/Nav.vue';
import BootstrapVue from 'bootstrap-vue'
import { AgGridVue } from '@ag-grid-community/vue';
import { AllCommunityModules } from '@ag-grid-community/all-modules';

import '@ag-grid-community/all-modules/dist/styles/ag-grid.css';
import '@ag-grid-community/all-modules/dist/styles/ag-theme-balham.css';
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false;

Vue.component('modal', {
  template: '#modal-template'
})


new Vue({
  router,
  render: h => h(App),
}).$mount('#app');

new Vue({
  router,
  render: h => h(Nav),
}).$mount('#navigation');

// - POPOUT
//
// function load_input_form() {
// //        $('#sidebar').toggleClass('active')
//   const xhttp = new XMLHttpRequest();
//   xhttp.onreadystatechange = function () {
//     if (this.readyState == 4 && this.status == 200) {
//       document.getElementById('side_panel_content').innerHTML = this.responseText;
//     }
//   };
//   xhttp.open('GET', '/input-form', true);
//   xhttp.send();
// }
//
//
// // - POPOUT
//
// function openNav() {
//   document.getElementById('mySidepanel').style.width = '500px';
//   load_input_form();
// }
//
// function closeNav() {
//   document.getElementById('mySidepanel').style.width = '0';
//   document.getElementById('detailPanel').style.width = '0';
// }
