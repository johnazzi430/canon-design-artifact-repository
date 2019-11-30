
<template>
  <div class="wrapper">
    <!-- LEFT SIDEPANEL -->
    <nav id="left-sidepanel" class="sidepanel-left">
      <a href="javascript:void(0)" id="Cards"
        class="nav-link active" v-on:click="changeView('card'); closeNav()">
          <!-- class="nav-link active" v-on:click="changeView('card')"> -->
        <i class="fa fa-user"></i></a>
      <a href="javascript:void(0)" id="Table"
        class="nav-link active" v-on:click="changeView('table') ">
        <i class="fa fa-list"></i></a>
      <a href="javascript:void(0)" id="Detail"
        class="nav-link active" v-on:click="expandDetail()">
        <i class="fa fa-align-left"></i></a>
      <a href="javascript:void(0)" id="Add"
          class="nav-link active" v-on:click=" refreshData(); expandDetail()"
          data-toggle="tooltip" title="Add">
      <i class="fa fa-plus"></i>
      </a>
    </nav>
      <!-- MAIN -->
    <div id="persona-panel" class="container-fluid" v-if="view === 'table'" v-bind:key="view">
      <div >
        <b-modal id="my-modal">
          <persona-add></persona-add>
        </b-modal>
        <persona-data></persona-data>
      </div>
    </div>
    <div class="" v-if="view === 'card'" v-bind:key="view">
      <persona-card></persona-card>
    </div>
    <!-- RIGHT SIDEPANEL -->
    <div id="right-sidepanel" class="sidepanel-right">
      <a href="javascript:void(0)"
        class="closebtn" @click="refreshData(); closeDetail(); ">&times;</a>
      <div id = "side-panel-switcher">
        <persona-detail :key="componentKey"></persona-detail>
      </div>
    </div>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  </div>
</template>

<!-- onClick="closeNav()" -->

<script>
/*eslint-disable */
import axios from 'axios'
import Table from './Personas/Table.vue';
import ViewDetail from './Personas/ViewDetail.vue';
import CardView from './Personas/CardView.vue';
import {EventBus} from "../event-bus.js";


export default {
  name: 'persona-panel',
  components: {
    'persona-data': Table,
    'persona-detail': ViewDetail,
    'persona-card': CardView,
  },
  data() {
    return {
     componentKey: 0,
     view:'card'
   }
  },
  methods: {
    closeDetail() {
    document.getElementById("right-sidepanel").style.width = "0px";
    },

    closeNav() {
    document.getElementById("left-sidepanel").style= "left: -115px"
    },

    expandDetail() {
    document.getElementById("right-sidepanel").style.width = "80%";
    },

    refreshData() {
      this.componentKey += 1;
      EventBus.$emit('selection-changed',this.selectedRow = '0')
    },

    changeView(view) { this.view = view},
  }
}


//document.getElementById("personaDetails").innerHTML = 'test';
EventBus.$on('selection-changed' , function() {document.getElementById("right-sidepanel").style.width = "500px"});

function closeNav() {
  document.getElementById("right-sidepanel").style.width = "0px";
}

</script>

<style scoped>

.sidepanel-right{
  height: 100%; /* Specify a height */
  width: 0; /* 0 width - change this with JavaScript */
  position: fixed; /* Stay in place */
  top: 0 ;
  z-index: 1; /* Stay on top */
  right: -16px;
  background-color: #f7f7f7; /* Black*/
  overflow-x: hidden; /* Disable horizontal scroll */
  padding-top: 75px; /* Place content 60px from the top */
  transition: 0.5s; /* 0.5 second transition effect to slide in the sidepanel */
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}

/* Style the links inside the sidenav */
.sidepanel-left{
  height: 100vh;
  z-index: 2;
  top: 0 ;
  left: -115px; /* Position them outside of the screen */
  transition: 0.3s; /* Add transition on hover */
  padding: 15px; /* 15px padding */
  padding-top: 100px;
  width: 40px; /* Set a specific width */
  background-color: #f7f7f7;
  text-decoration: none; /* Remove underline */
  overflow: hidden;
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
  margin-top:-15px;
  padding-top:-15px;
}

.wrapper {
    display: flex;
    width: 100%;
    align-items: stretch;
    margin-top:-16px;
    padding-top:-16px;
}

</style>
