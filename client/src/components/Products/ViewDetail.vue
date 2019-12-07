
<template>
<div style="padding-right:15px; margin-left:15px">
    <b-form id='product-detail'
        @submit="onEdit"
        @reset="onReset"
        @archive="onArchive">
      <div id='product-detail-show' v-if='editing === false && form.id != null'>
      <h1>Detail</h1>
      <span> Product ID: {{form.id}} | Revision: {{form.revision}}  </span>
      <div>
        <label>Name</label>
        <p class="text-wrap"> {{form.name}} </p>
        <label>Description</label>
        <p class="text-wrap"> {{form.description}} </p>
        <label>Metrics</label>
        <p class="text-wrap"> {{form.metrics}} </p>
        <label>Product Features</label>
        <p class="text-wrap"> {{form.features}} </p>
        <label>Goals</label>
        <p class="text-wrap"> {{form.goals}} </p>
        <label for="function">Owner</label>
        <p class="text-wrap"> {{form.owner}} </p>
        <label> Product Homepage</label>
        <p> {{form.product_homepage}} </p>
        <div v-for="persona in form.personas" v-bind:key="persona.persona_id">
          <b-button pill variant="info">{{persona.persona_title}} </b-button>
        </div>
      </div>
      <b-button href="javascript:void(0)" v-on:click="editing = true">Edit</b-button>

      <hr>
      <h4>Comments</h4>
      <comment-view :key='form.id'
                    v-bind:sourceTable="source"
                    v-bind:itemId='form.id'></comment-view>

    </div>
      <div  id='product-detail-edit' v-else>
        <h1 v-if='form.id != null'>Edit</h1>
        <h1 v-else>Add</h1>
        <div>
          <label>Name</label>
          <b-form-input v-model="form.name"></b-form-input>
          <label>Description</label>
          <b-form-textarea v-model="form.description"></b-form-textarea>
          <label>Metrics</label>
          <b-form-textarea v-model="form.metrics"></b-form-textarea>
          <label>Product Features</label>
          <b-form-textarea v-model="form.features"></b-form-textarea>
          <label>Goals</label>
          <b-form-input v-model="form.goals"></b-form-input>
          <label for="function">Owner</label>
          <b-form-input v-model="form.owner"></b-form-input>
          <label> Product Homepage</label>
          <b-form-input v-model="form.product_homepage"></b-form-input>
          <br>
          <multiselect
                      v-model="form.personas" :options="persona_options"
                      :multiple="true" :close-on-select="false"
                      :clear-on-select="false" :preserve-search="true"
                      placeholder="Pick some" label="persona_title"
                      track-by="persona_id" :preselect-first="false">
            <template slot="selection"
                      slot-scope="{ values, search, isOpen }">
              <span class="multiselect__single"
                    v-if="values.length &amp;&amp; !isOpen">
                          {{ values.length}} options selected
                        </span>
            </template>
          </multiselect>
          <br>
          <div >Selected: <strong>{{ form.persona}}</strong></div>
        </div>
        <div >
          <label for="product_file">Add File</label>
          <b-form-file v-model="form.product_file"
          :state="Boolean(form.product_file)"
          name="product_file"
          placeholder="Choose a file or drop it here..."
          drop-placeholder="Drop file here..."></b-form-file>
        </div>
        <br>
        <div id="button-if" v-if='form.id != null'>
          <b-button type="reset" variant="secondary">Return</b-button>
          <b-button href="javascript:void(0)"
            type="button" variant="danger"  v-on:click='onArchive'> Archive</b-button>
          <b-button href="javascript:void(0)"
            type="submit" variant="primary" v-on:click='onEdit'>Submit Changes</b-button>
        </div>
        <div class="" v-else>
          <b-button type="submit" variant="primary">Add New Persona</b-button>
        </div>
      </div>
  </b-form>

</div>
</template>

<script>
/*eslint-disable */
import axios from 'axios'
import CommentView from '../CommentView.vue'
import {EventBus} from "../../index.js";

export default {
  name: "product-details",
  components : {'comment-view': CommentView },
  data() {
    return {
      form: {
        id: null,
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
        personas: '',
        product_photo: '',
        product_file: null},
      editing: false,
      source: 'product',
      persona_options : []
      }
    },
    beforeMount() {
      const self = this;

      // SET OPTIONS
      axios.get("/api/personas")
        .then(response => {
          self.persona_options = response.data;
        })
        .catch(error => console.log(error))

      // GET ON DATA CHANGE
      EventBus.$on('selection-changed', function(selection){

        var get_url = "/api/product-table/";
        get_url += selection;

        axios.get(get_url)
        .then(response => {
            self.form.id = selection;
            self.form.name = response.data[0].name;
            self.form.description= response.data[0].description;
            self.form.metrics= response.data[0].metrics;
            self.form.goals= response.data[0].goals;
            self.form.features = response.data[0].features;
            self.form.owner = response.data[0].owner;
            self.form.product_homepage = response.data[0].product_homepage;
            self.form.revision= response.data[0].revision;
            self.editing = false;
          }
        )
        .catch(error => console.log(error))
        });
      },
      methods: {
       onEdit(evt) {
         evt.preventDefault()
         axios({
             method: 'post',
             url: '/api/product-table',
             data: this.form, })
         .then(function (response) {
             console.log(response);})
         .catch(function (error) {
             console.log(error);})

        axios({
            method: 'post',
            url: '/api/persona-product',
            data: this.form,
            params : {
                table : "product"
              }
            })
        .then(function (response) {
            console.log(response);})
        .catch(function (error) {
            console.log(error);})

         EventBus.$emit('product-table-changed','item-updated')
         document.getElementById("right-sidepanel").style.width = "0px";
       },

       onAdd(evt) {
         evt.preventDefault()
         axios({
             method: 'post',
             url: '/api/product-table',
             data: this.form, })
         .then(function (response) {
             console.log(response);})
         .catch(function (error) {
             console.log(error);})

         EventBus.$emit('product-table-changed','item-updated')
         document.getElementById("right-sidepanel").style.width = "0px";
       },

       onReset(evt) {
         evt.preventDefault()
         // Reset our form values
         this.editing = false;
       },

       onArchive(evt) {
         evt.preventDefault()
         var get_url = '/api/product-table/';
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
         EventBus.$emit('product-table-changed' , archive_set )
         document.getElementById("right-sidepanel").style.width = "0px";
      },
     },
  };

</script>


<style scoped>

.avatar {
  vertical-align: middle;
  text-align: center;
  width: 100px;
  height: 100px;
  border-radius: 50%;
};

p {
  white-space: pre-line;
};


</style>
