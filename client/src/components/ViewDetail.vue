
TODO: fix switching

<template>
<div class="conatainer-fluid">
    <b-form id='persona-detail'
        @submit="onSubmit"
        @reset="onReset"
        @archive="onArchive">
      <div class="container" id='persona-detail-show' v-if='editing === false'>
      <h1>Detail</h1>
      <span> User ID: {{form.id}} | Revision: {{form.revision}}  </span>
      <div>
        <label for="Name">Name</label>
        <p> {{form.name}} </p>
      </div>
      <div>
        <label for="Title">Title</label>
        <p> {{form.title}} </p>
      </div>
      <div>
        <label for="external">Internal or External?</label>
        <b-form-radio v-model="form.external" name="some-radios"
        value="1">External</b-form-radio>
        <b-form-radio v-model="form.external" name="some-radios"
        value="0">Internal</b-form-radio>
      </div>
      <div>
        <label for="qty">Number people who fit this persona</label>
        <p> {{form.market_size}} </p>
      </div>
      <div>
        <label for="quote">Persona Quote</label>
        <p> {{form.quote}} </p>
      </div>
      <div>
        <label for="function">Job Function</label>
        <p> {{form.job_function}} </p>
      </div>
      <div>
        <label for="needs">Needs</label>
        <p> {{form.needs}} </p>
      </div>
      <div>
        <label for="wants">Wants</label>
        <p> {{form.wants}} </p>
      </div>
      <div>
        <label for="pain_point">Pain Points</label>
          <p> {{form.pain_point}} </p>
      </div>
      <div>
        <label for="buss_val">value to business</label>
        <b-form-input type="range" min="0" max="5" v-model="form.buss_val" />
      </div>
      <div>
        <label for="persona_file">Add File</label>
        <p> {{form.persona_file}} </p>
      </div>
      <b-button href="javascript:void(0)" v-on:click="editing = true">Edit</b-button>
    </div>
      <div class="container" id='persona-detail-edit' v-else>

        <h1>Edit</h1>
        <div>
          <label for="Name">Name</label>
          <b-form-input v-model="form.name"  name="Name" />
        </div>
        <div>
          <label for="Title">Title</label>
          <b-form-input v-model="form.title" id="Title" name="Title" />
        </div>
        <div>
          <label for="external">Internal or External?</label>
          <b-form-radio v-model="form.external" name="some-radios"
          value="1">External</b-form-radio>
          <b-form-radio v-model="form.external" name="some-radios"
          value="0">Internal</b-form-radio>
        </div>
        <div>
          <label for="qty">Number people who fit this persona</label>
          <b-form-input type="number" v-model="form.market_size" id="qty" name="qty" />
        </div>
        <div>
          <label for="quote">Persona Quote</label>
          <b-form-textarea v-model="form.quote" id="quote" name="quote" />
        </div>
        <div>
          <label for="function">Job Function</label>
          <b-form-textarea v-model="form.job_function" id="function" name="function" />
        </div>
        <div>
          <label for="needs">Needs</label>
          <b-form-textarea v-model="form.needs" id="needs" name="needs" />
        </div>
        <div>
          <label for="wants">Wants</label>
          <b-form-textarea v-model="form.wants" id="wants" name="wants" />
        </div>
        <div>
          <label for="pain_point">Pain Points</label>
          <b-form-textarea v-model="form.pain_point" id="pain_point" name="pain_point" />
        </div>
        <div>
          <label for="buss_val">value to business</label>
          <b-form-input type="range" min="0" max="5" v-model="form.buss_val" />
        </div>
        <div>
          <label for="persona_file">Add File</label>
          <b-form-file v-model="form.persona_file"
          :state="Boolean(form.persona_file)"
          name="persona_file"
          placeholder="Choose a file or drop it here..."
          drop-placeholder="Drop file here..."></b-form-file>
        </div>
        <br>
        <b-button type="button" variant="danger"  v-on:click='onArchive'> Archive</b-button>
        <b-button type="reset" variant="secondary">Reset</b-button>
        <b-button type="submit" variant="primary">Submit</b-button>
      </div>
  </b-form>
</div>
</template>

<script>
/*eslint-disable */
import axios from 'axios'
import {EventBus} from "../event-bus.js";

export default {
  name: "persona-details",
  data() {
    return {
      form: {
        name: '',
        title: '',
        external: '',
        market_size: '',
        quote: '',
        job_function: '',
        needs: '',
        wants: '',
        pain_point: '',
        buss_val: '',
        revision: '',
        persona_file: null},
      editing: false
      }
    },
    beforeMount() {
      const self = this;
      EventBus.$on('selection-changed', function(selection){

        var get_url = "http://localhost:5000/api/persona-table/";
        get_url += selection;

        axios.get(get_url)
        .then(response => {
            self.form.id = selection;
            self.form.name = response.data[0].name;
            self.form.title= response.data[0].title;
            self.form.market_size= response.data[0].market_size;
            self.form.quote = response.data[0].quote;
            self.form.job_function = response.data[0].job_function;
            self.form.needs = response.data[0].needs;
            self.form.wants = response.data[0].wants;
            self.form.pain_point= response.data[0].pain_point;
            self.form.buss_val= response.data[0].buss_val;
            self.form.revision= response.data[0].revision;
            self.editing = false;
          }
        )
        .catch(error => console.log(error))
        });
      },
      methods: {
       onSubmit(evt) {
         evt.preventDefault()
         axios({
             method: 'post',
             url: 'http://localhost:5000/api/persona-table',
             data: this.form, })
         .then(function (response) {
             console.log(response);})
         .catch(function (error) {
             console.log(error);})
       },

       onReset(evt) {
         evt.preventDefault()
         // Reset our form values
         this.form.name = ''
         this.form.title = ''
         this.form.external = ''
         this.form.qty = ''
         this.form.quote = ''
         this.form.job_function = ''
         this.form.needs = ''
         this.form.wants = ''
         this.form.pain_point = ''
         this.form.buss_val = ''
         this.form.persona_file = null
       },

       onArchive(evt) {

         evt.preventDefault()
         var get_url = 'http://localhost:5000/api/persona-table/';
         get_url += this.form.id ;
         //get_url += '?name=frank';

         var archive_set = { 'archived': 1};

         console.log(get_url)
         axios({
             method: 'PUT',
             url: get_url,
             data: archive_set,
            })
         .then(function (response) {
             console.log(response);})
         .catch(function (error) {
             console.log(error);})

         console.log('delete')
      },
     },
  };

</script>
