
<template>
  <div class="">
    <!-- LEFT SIDEPANEL -->
    <div id="left-sidepanel" class="sidepanel-left">
      <a href="#" id="Cards" class="row"><i class="fa fa-fw fa-user"></i> Cards</a>
      <a href="#" id="Table" class="row"><i class="fa fa-list"></i> Table</a>
      <a href="#" id="Detail" class="row"> <i class="fa fa-align-left"></i> Detail</a>
    </div>
      <!-- MAIN -->
    <div id="persona-panel" class="container-fluid" @close="closeNav()">
      <div >
        <b-button v-b-modal.my-modal pill variant="outline-secondary" >Add Data</b-button>
        <b-modal id="my-modal">
          <persona-add></persona-add>
        </b-modal>
        <persona-data></persona-data>
      </div>
    </div>
    <!-- RIGHT SIDEPANEL -->
    <div id="right-sidepanel" class="sidepanel-right">
      <a href="javascript:void(0)" class="closebtn" @click="closeNav()">&times;</a>
      <div id = "side-panel-switcher">
        <persona-detail></persona-detail>
      </div>
    </div>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  </div>
</template>

<!-- onClick="closeNav()" -->

<script>
/*eslint-disable */
import axios from 'axios'
import Table from './Table.vue';
import InputForm from './InputForm.vue';
import ViewDetail from './ViewDetail.vue';
import {EventBus} from "../event-bus.js";


export default {
  name: 'persona-panel',
  components: {
    'persona-data': Table,
    'persona-add': InputForm,
    'persona-detail': ViewDetail,
  },
  methods: { closeNav() {
    document.getElementById("right-sidepanel").style.width = "0px";
  }}
}

//document.getElementById("personaDetails").innerHTML = 'test';
EventBus.$on('selection-changed' , function() {document.getElementById("right-sidepanel").style.width = "500px"});

function closeNav() {
  document.getElementById("right-sidepanel").style.width = "0px";
}

</script>

<style>

.sidepanel-right{
  height: 100%; /* Specify a height */
  width: 0; /* 0 width - change this with JavaScript */
  position: fixed; /* Stay in place */
  z-index: 1; /* Stay on top */
  top: 0;
  right: -16px;
  background-color: #f7f7f7; /* Black*/
  overflow-x: hidden; /* Disable horizontal scroll */
  padding-top: 60px; /* Place content 60px from the top */
  padding: 16px;
  transition: 0.5s; /* 0.5 second transition effect to slide in the sidepanel */
}

/* Style the links inside the sidenav */
.sidepanel-left{
  height: 100%;
  position: fixed;  /* Position them relative to the browser window */
  z-index: 1;
  top: 0;
  left: -115px; /* Position them outside of the screen */
  transition: 0.3s; /* Add transition on hover */
  padding: 30px; /* 15px padding */
  width: 130px; /* Set a specific width */
  background-color: #f7f7f7;
  text-decoration: none; /* Remove underline */
  overflow-x: hidden;
  font-size: 20px; /* Increase font size */
  color: white; /* White text color */
  align-content: left;

}

.sidepanel-left:hover {
  left: 0; /* On mouse-over, make the elements appear as they should */
}

#persona_panel {
  padding-left:15px;
  margin-left:15px;
  padding-right:15px;
  margin-right:15px;
}

</style>
