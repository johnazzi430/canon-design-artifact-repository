<template>
  <div class="wrapper">
    <!-- LEFT SIDEPANEL -->
    <nav id="left-sidepanel" class="sidepanel-left">
      <a href="javascript:void(0)" id="Cards"
        class="nav-link active" v-on:click="changeView('card'); closeNav()">
          <!-- class="nav-link active" v-on:click="changeView('card')"> -->
        <i class="fa fa-exclamation"></i></a>
      <!-- v-if start -->
      <div v-if="this.selection !== null">
        <a href="javascript:void(0)" id="Detail"
          class="nav-link active" v-on:click="expandDetail()">
          <i class="fa fa-align-left"></i>
        </a>
      </div>
      <div v-else>
        <a href="javascript:void(0)" id="Detail"
            class="nav-link disabled" v-on:click="expandDetail()">
            <i class="fa fa-align-left"></i>
        </a>
      </div>
      <!-- v-if start -->
      <a href="javascript:void(0)" id="Add"
          class="nav-link active"
          v-on:click=" addDataAction();  expandDetail()"
          data-toggle="tooltip" title="Add">
      <i class="fa fa-plus"></i></a>
      <a href="javascript:void(0)" id="Dashboard"
          class="nav-link disabled" v-on:click="expandDetail()">
          <i class="fas fa-chart-line"></i></a>
    </nav>
      <!-- MAIN -->
    <div class="" v-if="view === 'card'" v-bind:key="view">
      <insight-card v-bind:key = "dataKey">></insight-card>
    </div>
    <!-- RIGHT SIDEPANEL -->
    <div id="right-sidepanel" class="sidepanel-right">
      <h1><a href="javascript:void(0)"
        class="closebtn" @click="closeDetail(); ">&times;</a></h1>
      <div id = "side-panel-switcher">
        <insight-detail :key="detailKey"></insight-detail>
      </div>
    </div>
  </div>
</template>

<!-- onClick="closeNav()" -->

<script>
/*eslint-disable */
import axios from 'axios'
import ViewDetail from './Insights/ViewDetail.vue';
import CardView from './Insights/CardView.vue';
import {EventBus} from "../index.js";


export default {
  name: 'insight-panel',
  components: {
    'insight-detail': ViewDetail,
    'insight-card': CardView,
  },
  data() {
    return {
    detailKey: 0,
    dataKey: 0,
    view:'card',
    selection: 0,
   }
  },
  methods: {

    expandDetail() {
    document.getElementById("right-sidepanel").style.width = "80%";
    },

    closeDetail() {
    document.getElementById("right-sidepanel").style.width = "0px";
    },

    closeNav() {
    document.getElementById("left-sidepanel").style= "left: -115px"
    },

    addDataAction() {
      this.detailKey += 1;
      EventBus.$emit('insight-selection-changed',this.selectedRow = null)
    },

    changeView(view) { this.view = view},
  },
  mounted() {

    const self = this;

    EventBus.$on('insight-selection-changed' , function(selection) {
      document.getElementById("right-sidepanel").style.width = "500px"
      self.selection = selection
    })
  },
}


function closeNav() {
  document.getElementById("right-sidepanel").style.width = "0px";
}

</script>

<style lang="scss" scoped>

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
  width: 60px; /* Set a specific width */
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

// #insight_panel {
//   padding-left:15px;
//   margin-left:15px;
//   padding-right:15px;
//   margin-right:15px;
//   margin-top:-15px;
//   padding-top:-15px;
// }

.wrapper {
    display: flex;
    width: 100%;
    align-items: stretch;
    margin-top:-16px;
    padding-top:-16px;
}

</style>
