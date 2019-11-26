
<template>
  <div class="conatainer-fluid">
    <!-- <div? v-for="item in data"> -->
    <!-- <div>
      <div class="card">
        <div id='persona-detail'>
          <div class="container" id='persona-detail-show' v-if='editing === false'>
            <h1>Detail</h1>
            <span> User ID: {{form.id}} | Revision: {{form.revision}}  </span>
            <label for="Name">Name</label>
            <p> {{form.name}} </p>
            <br>
            <label for="Title">Title</label>
            <p> {{form.title}} </p>
            <br>
            <label for="external">Internal or External?</label>
            <b-form-radio v-model="form.external" name="some-radios"
            value="1">External</b-form-radio>
            <b-form-radio v-model="form.external" name="some-radios"
            value="0">Internal</b-form-radio>
            <br>
            <label for="qty">Number people who fit this persona</label>
            <p> {{form.market_size}} </p>
            <br>
            <label for="quote">Persona Quote</label>
            <p> {{form.quote}} </p>
            <br>
            <label for="function">Job Function</label>
            <p> {{form.job_function}} </p>
            <br>
            <label for="needs">Needs</label>
            <p> {{form.needs}} </p>
            <br>
            <label for="wants">Wants</label>
            <p> {{form.wants}} </p>
            <br>
            <label for="pain_point">Pain Points</label>
            <p> {{form.pain_point}} </p>
            <br>
            <label for="buss_val">value to business</label>
            <b-form-input type="range" min="0" max="5" v-model="form.buss_val" />
            <br>
            <label for="persona_file">Add File</label>
            <p> {{form.persona_file}} </p>
          </div>
          <b-button href="javascript:void(0)" v-on:click="editing = true">Edit</b-button>
        </div>
      </div>
    </div> -->
  </div>
</template>

<script>
/*eslint-disable */
import axios from 'axios'
import {EventBus} from "@/event-bus.js";

export default {
  name: "persona-detail",
  data() {
    items: [ {data:''} ]
    },
    beforeMount() {
        get_url = "http://localhost:5000/api/persona-table/";

        axios.get(get_url)
          .then(response => {
            self.form = response.data
            }
          )
          .catch(error => console.log(error))
      },
   };

</script>
