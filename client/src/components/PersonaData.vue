
<template>
  <div id="persona_panel">
    <div >
      <b-button v-b-modal.my-modal>Add Data</b-button>
      <b-modal id="my-modal">
        <persona-add></persona-add>
      </b-modal>
      <persona-data></persona-data>
    </div>
    <div id="mySidepanel" class="sidepanel">
        <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
        <persona-detail></persona-detail>
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


//document.getElementById("personaDetails").innerHTML = 'test';
EventBus.$on('selection-changed' , function() {document.getElementById("mySidepanel").style.width = "500px"});

function closeNav() {
  document.getElementById("mySidepanel").style.width = "0";
}

export default {
  name: 'persona_panel',
  components: {
    'persona-data': Table,
    'persona-add': InputForm,
    'persona-detail': ViewDetail,
  },
}

</script>
