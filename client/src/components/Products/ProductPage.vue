
<template>
  <div class="wrapper">
    <!-- LEFT SIDEPANEL -->
    <b-nav id="left-sidepanel" vertical class="sidepanel-left">
      <b-nav-item href="javascript:void(0)" id="Cards"
        class="nav-link active" v-on:click="changeView('card')">
          <!-- class="nav-link active" v-on:click="changeView('card')"> -->
        <i class="fa fa-laptop nav-icon"></i>
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
            <i class="fas fa-align-left nav-icon"></i>
            <span class="nav-text">Details</span>
      </b-nav-item>
      <b-nav-item v-else href="javascript:void(0)" id="Detail"
              class="nav-link disabled" v-on:click="expandDetail() ">
              <i class="fa fa-align-left nav-icon"></i>
              <span class="nav-text">Details</span>
      </b-nav-item>
        <!-- v-if start -->
      <b-nav-item href="javascript:void(0)" id="Add"
          v-if="this.$store.getters.isLoggedIn"
          class="nav-link active" v-on:click=" addDataAction(); expandDetail()"
          data-toggle="tooltip" title="Add">
      <i class="fa fa-plus nav-icon"></i>
      <span class="nav-text">Add New</span>
      </b-nav-item>
    </b-nav>
      <!-- MAIN -->
      <div id = "main" class ="main">
        <div id="product-panel"  v-if="view === 'table'" v-bind:key="view">
            <product-data :rowData="products" v-bind:key = "dataKey"></product-data>
        </div>
        <div v-if="view === 'card'" v-bind:key="view">
          <product-card :cards="products" v-bind:key = "dataKey"></product-card>
        </div>
      </div>
    <!-- RIGHT SIDEPANEL -->
    <div id="right-sidepanel" class="sidepanel-right">
      <h1><a href="javascript:void(0)"
        class="closebtn" @click="closeDetail(); ">&times;</a></h1>
      <div id = "side-panel-switcher">
        <product-detail :key="detailKey"></product-detail>
      </div>
    </div>
  </div>
</template>

<!-- onClick="closeNav()" -->

<script>
/*eslint-disable */
import axios from 'axios'
import api from '../../api'
import Table from './Table.vue';
import ViewDetail from './ViewDetail.vue';
import CardView from './CardView.vue';
import {EventBus} from "../../index.js";


export default {
  name: 'product-panel',
  components: {
    'product-data': Table,
    'product-detail': ViewDetail,
    'product-card': CardView,
  },
  data() {
    return {
     products: [],
     detailKey: 0,
     dataKey: 0,
     view:'card',
     selection : null
   }
  },
  watch: {
    $route(to, from) {
      EventBus.$emit('product-selection-changed',this.selectedRow = this.$route.params.id )
    }
  },
  async beforeMount() {
    const {data} = await api.productTable()
    this.products = data

    let self = this
    EventBus.$on('persona-data-changed', async function(){
      const {data} = await api.productTable()
      self.products = data
    })
  },
  methods: {

    expandDetail() {
      document.getElementById("right-sidepanel").style.width = "80%";
    },

    closeDetail() {
      document.getElementById("right-sidepanel").style.width = "0px";
      // EventBus.$emit('selection-changed',this.selectedRow = null);
    },

    closeNav() {
      document.getElementById("right-sidepanel").style.width = "0px";
    },

    addDataAction() {
      this.detailKey += 1;
      EventBus.$emit('product-selection-changed',this.selectedRow = null)
    },

    changeView(view) { this.view = view},
  },
  mounted () {
    const self = this

    EventBus.$on('product-selection-changed' , function(selection) {
      document.getElementById("right-sidepanel").style.width = "50%"
      self.selection = selection
    });

    if(this.$route.params.id)
      {EventBus.$emit('product-selection-changed',this.selectedRow = this.$route.params.id)};
  }
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
  margin-left: 0px;
  position:fixed;
  width: 60px;
  height: 100vh;
  background-color: #F7F7F7;
  border-right-style: solid;
  border-right-color: #D1D1D1;
  border-right-width: thin;
  white-space: nowrap;
  overflow-x: hidden;
}

.nav-text{
  width:60px;
  padding-left:10px;
}

.nav-icon{
  width:50px;
  margin-right:10px
}

.nav-link{
  padding:15px 0px;
  font-size: 15px;
}

.sidepanel-left:hover {
  width: 170px; /* On mouse-over, make the elements appear as they should */
  transition: 0.25s;
}

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
