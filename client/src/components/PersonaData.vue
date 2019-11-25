
<template>
  <div id="persona_panel" @close="closeNav()">
    <div >
      <b-button v-b-modal.my-modal pill variant="outline-secondary" >Add Data</b-button>
      <b-modal id="my-modal">
        <persona-add></persona-add>
      </b-modal>
      <persona-data></persona-data>
    </div>
    <div id="mySidepanel" class="sidepanel">
        <a href="javascript:void(0)" class="closebtn" @click="closeNav()">&times;</a>
      <div id = "side-panel-switcher">
        <persona-detail></persona-detail>
      </div>
    </div>
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
  name: 'persona_panel',
  components: {
    'persona-data': Table,
    'persona-add': InputForm,
    'persona-detail': ViewDetail,
  },
  methods: { closeNav() {
    document.getElementById("mySidepanel").style.width = "0px";
  }}
}

//document.getElementById("personaDetails").innerHTML = 'test';
EventBus.$on('selection-changed' , function() {document.getElementById("mySidepanel").style.width = "500px"});

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
  right: -16px;
  background-color: #f7f7f7; /* Black*/
  overflow-x: hidden; /* Disable horizontal scroll */
  padding-top: 60px; /* Place content 60px from the top */
  padding: 16px;
  transition: 0.5s; /* 0.5 second transition effect to slide in the sidepanel */
}


</style>
