b-nav-item<template>
  <div class="wrapper">
    <!-- LEFT SIDEPANEL -->
    <b-nav id="left-sidepanel" vertical class="sidepanel-left">
      <b-nav-item href="javascript:void(0)" id="Cards"
        class="nav-link active" v-on:click="changeView('card'); closeNav()">
          <!-- class="nav-link active" v-on:click="changeView('card')"> -->
        <i class="fa fa-exclamation"></i>
      </b-nav-item>
      <!-- v-if start -->
      <b-nav-item v-if="this.selection !== null"
          href="javascript:void(0)" id="Detail"
          class="nav-link active" v-on:click="expandDetail()">
          <i class="fa fa-align-left"></i>
      </b-nav-item>
      <b-nav-item v-else href="javascript:void(0)" id="Detail"
            class="nav-link disabled" v-on:click="expandDetail()">
            <i class="fa fa-align-left"></i>
      </b-nav-item>
      <!-- v-if start -->
      <b-nav-item href="javascript:void(0)" id="Add"
          class="nav-link active"
          v-on:click=" addDataAction();  expandDetail()"
          data-toggle="tooltip" title="Add">
          <i class="fa fa-plus"></i>
      </b-nav-item>
      <b-nav-item href="javascript:void(0)" id="Dashboard"
          class="nav-link disabled" v-on:click="expandDetail()">
          <i class="fas fa-chart-line"></i>
        </b-nav-item>
    </b-nav>
    <div class ="main">
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
    selection: null,
   }
  },
  watch: {
    '$route' (to, from) {
      EventBus.$emit('insight-selection-changed',this.selectedRow = this.$route.params.id )
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

    EventBus.$on('insight-data-changed' , function(selection) {
      self.dataKey =+ 1;
    })

    if(this.$route.params.id)
      {EventBus.$emit('insight-selection-changed',this.selectedRow = this.$route.params.id)};
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
  position:fixed;
  width: 60px;
  height:100%;
  background-color: #F7F7F7;
  border-right-style: solid;
  border-right-color: #D1D1D1;
  border-right-width: thin;
}

.sidepanel-left:hover {
  width: 160px; /* On mouse-over, make the elements appear as they should */
  transition: 0.25s;
}


// .sidepanel-left:hover {
//   width: 160px; /* On mouse-over, make the elements appear as they should */
// }

.main{
  width: 100%;
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
