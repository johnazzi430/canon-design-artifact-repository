/*eslint-disable */
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import { AgGridVue } from '@ag-grid-community/vue';
import { AllCommunityModules } from '@ag-grid-community/all-modules';

import '@ag-grid-community/all-modules/dist/styles/ag-grid.css';
import '@ag-grid-community/all-modules/dist/styles/ag-theme-balham.css';

Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');


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
