
<template>
  <div id="persona_panel" class="container-fluid" @close="closeNav()">
    <div>
      <b-button v-b-modal.my-modal pill variant="outline-secondary" >Add Data</b-button>
      <b-button v-on:click="onRefresh()"
      pill variant="outline-secondary" >Refresh Data</b-button>
      <b-modal id="my-modal">
        <persona-add></persona-add>
      </b-modal>
    </div>
    <persona-data></persona-data>
    <div class="wrapper">
      <div id="mySidepanel"
      class="sidepanel container"
      style="width:0px">
      <div class="row">
        <div class="col overflow:auto">
          <a href="javascript:void(0)" class="closebtn" @click="closeNav()"
          style="padding:0px; magin:-16px; font-size:25px; ">
          <span class="glyphicon glyphicon-arrow-left"></span>
          return</a>
          <div id = "side-panel-switcher">
            <persona-detail></persona-detail>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>


<script>
/*eslint-disable */
import axios from 'axios'
import Table from './Table.vue';
import InputForm from './InputForm.vue';
import ViewDetail from './ViewDetail.vue';
import {EventBus} from "../event-bus.js";


export default {
  name: 'persona_panel',
  components: {
    'persona-data': Table,
    'persona-add': InputForm,
    'persona-detail': ViewDetail,
  },
  methods: { closeNav() {
    document.getElementById("mySidepanel").style.width = "0px";
  },

  onRefresh() {
    EventBus.$on('persona-table-changed',function(){console.log('persona table changed')})
  },
 }
}

//document.getElementById("personaDetails").innerHTML = 'test';
EventBus.$on('selection-changed' , function() {document.getElementById("mySidepanel").style.width = "40%"});

function closeNav() {
  document.getElementById("mySidepanel").style.width = "0px";
}


</script>

<style>

.sidepanel {
  height: 100%; /* Specify a height */
  width: 0; /* 0 width - change this with JavaScript */
  position: fixed; /* Stay in place */
  z-index: 1; /* Stay on top */
  top: 0;
  right: 0px;
  background-color: #f7f7f7;
  overflow-x: hidden; /* Disable horizontal scroll */
  padding: 16px;
  transition: 0.5s; /* 0.5 second transition effect to slide in the sidepanel */
}

</style>
