
<template>
  <div class="wrapper">
    <!-- LEFT SIDEPANEL -->
    <b-nav id="left-sidepanel" vertical class="sidepanel-left">
      <b-nav-item href="javascript:void(0)" id="Cards"
        class="nav-link active" v-on:click="changeView('card')">
          <!-- class="nav-link active" v-on:click="changeView('card')"> -->
        <i class="fa fa-user nav-icon"></i>
        <span class="nav-text">Cards</span>
      </b-nav-item>
      <b-nav-item href="javascript:void(0)" id="Table"
        class="nav-link active" v-on:click="changeView('table') ">
        <i class="fa fa-list nav-icon"></i>
        <span class="nav-text">Table</span>
      </b-nav-item>
      <!-- v-if start -->
      <b-nav-item v-if="this.selection !== null"
          href="javascript:void(0)" id="Detail"
          class="nav-link active" v-on:click="expandDetail()">
          <i class="fa fa-align-left nav-icon"></i>
          <span class="nav-text">Details</span>
      </b-nav-item>
      <b-nav-item v-else
            href="javascript:void(0)" id="Detail"
            class="nav-link disabled" v-on:click="expandDetail()">
            <i class="fa fa-align-left nav-icon"></i>
            <span class="nav-text">Details</span>
        </b-nav-item>
      <!-- v-if start -->
      <b-nav-item href="javascript:void(0)" id="Add"
          class="nav-link active"
          v-on:click=" addDataAction();  expandDetail()"
          data-toggle="tooltip" title="Add">
          <i class="fa fa-plus nav-icon"></i>
          <span class="nav-text">Add New</span>
      </b-nav-item>
    </b-nav>
      <!-- MAIN -->
    <div id = "main" class ="main">
      <div id="persona-panel"  v-if="view === 'table'" v-bind:key="view">
          <persona-data v-bind:key = "dataKey"></persona-data>
      </div>
      <div v-if="view === 'card'" v-bind:key="view">
        <persona-card v-bind:key = "dataKey">></persona-card>
      </div>
    </div>

    <!-- RIGHT SIDEPANEL -->
    <div id="right-sidepanel" class="sidepanel-right">
      <h1><a href="javascript:void(0)"
        class="closebtn" @click="closeDetail(); ">&times;</a></h1>
      <div id = "side-panel-switcher">
        <persona-detail :key="detailKey"></persona-detail>
      </div>
    </div>
  </div>
</template>

<!-- onClick="closeNav()" -->

<script>
/*eslint-disable */
import axios from 'axios'
import Table from './Table.vue';
import ViewDetail from './ViewDetail.vue';
import CardView from './CardView.vue';
import {EventBus} from "../../index.js";


export default {
  name: 'persona-panel',
  components: {
    'persona-data': Table,
    'persona-detail': ViewDetail,
    'persona-card': CardView,
  },
  data() {
    return {
    detailKey: 0,
    dataKey: 0,
    view:'card',
    selection: null,
   }
  },
  watch: {
    $route(to, from) {
      document.getElementById("right-sidepanel").style.width = "80%";
      EventBus.$emit('persona-selection-changed',this.selectedRow = this.$route.params.id )
    },
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
      EventBus.$emit('persona-selection-changed',this.selectedRow = null)
    },

    changeView(view) { this.view = view},
  },
  mounted() {

    const self = this;

    EventBus.$on('persona-selection-changed' , function(selection) {
      document.getElementById("right-sidepanel").style.width = "500px"
      self.selection = selection
    })

    if(this.$route.params.id)
      {EventBus.$emit('persona-selection-changed',this.selectedRow = this.$route.params.id)};
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
  background-color: #FFFFFF; /* Black*/
  overflow-x: hidden; /* Disable horizontal scroll */
  padding-top: 75px; /* Place content 60px from the top */
  padding-right: 15px;
  transition: 0.5s; /* 0.5 second transition effect to slide in the sidepanel */
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}

.sidepanel-left{
  z-index:1;
  left:0;
  top:0;
  padding-top: 70px;
  position:fixed;
  width: 60px;
  height: 100vh;
  overflow-x: hidden;
  background-color: #F7F7F7;
  border-right-style: solid;
  border-right-color: #D1D1D1;
  border-right-width: thin;
  white-space: nowrap;
}

.sidepanel-left:hover {
  width: 160px; /* On mouse-over, make the elements appear as they should */
  transition: 0.25s;
}

.nav-text{
  width:60px
}

.nav-icon{
  width:40px
}

.main{
  width: 100%;
  height: 100vh;
  margin-left: 60px;
  padding: 0px 10px;
  background-color: #F7F7F7
}


.wrapper {
    display: flex;
    width: 100%;
    align-items: stretch;
    margin-top:-16px;
    padding-top:-16px;
}

</style>
