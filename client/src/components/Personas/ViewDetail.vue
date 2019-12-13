
<template>
<div style="padding-right:15px; margin-left:15px">
    <b-form id='persona-detail'
        @submit="onEdit"
        @reset="onReset"
        @archive="onArchive">
      <div id='persona-detail-show' v-if='editing === false && form.id !== null'>
      <h1>Detail</h1>
      <span> Persona ID: {{form.id}} | Revision: {{form.revision}}  </span>
      <div class="">
        <div class="">
          <img src="../../../public/assets/img_avatar2.png" alt="Avatar" class="avatar">
        </div>
        <label for="Name">Name</label>
        <div class="panel-group"> {{form.name}} </div>
        <label for="Title">Title</label>
        <p class="text-wrap"> {{form.title}} </p>
        <label for="external">Internal or External?</label>
        <p class="text-wrap"> {{form.external}} </p>
        <label for="qty">Number people who fit this persona</label>
        <p> {{form.market_size}} </p>
        <label for="quote">Persona Quote</label>
        <p> {{form.quote}} </p>
        <label for="function">Job Function</label>
        <p class="text-wrap"> {{form.job_function}} </p>
        <label for="needs" style="white-space: pre-line;">Needs</label>
        <p> {{form.needs}} </p>
        <label for="wants" style="white-space: pre-line;">Wants</label>
        <p> {{form.wants}} </p>
        <label for="pain_point">Pain Points</label>
        <p> {{form.pain_point}} </p>
        <label for="buss_val">value to business</label>
        <b-form-input type="range" min="0" max="5" v-model="form.buss_val" />
        <label>Associated Products</label>
        <div v-for="product in form.products" v-bind:key="product.product_id">
          <b-button pill variant="info">{{product.product_name}}</b-button>
          <!-- TODO: make it so clicking her routes to the product -->
        </div>
        <label>Associated Roles</label>
        <div v-for="role in form.roles" v-bind:key="role.persona_role_id">
          <b-badge pill variant="success">{{role.persona_role_name}}</b-badge>
        </div>
        <div class="mt-2">Market Value: {{ form.buss_val }}</div>
        <label for="persona_file">Add File</label>
        <p> {{form.persona_file}} </p>
      </div>
      <b-button href="javascript:void(0)" v-on:click="editing = true">Edit</b-button>

      <hr>
      <h4>Comments</h4>
      <comment-view v-bind:sourceTable="source"
                    v-bind:itemId='form.id'></comment-view>

    </div>
      <div  id='persona-detail-edit' v-else>
        <h1 v-if='form.id === null'>Add</h1>
        <h1 v-else>Edit</h1>
        <div>
          <label for="Name">Name</label>
          <b-form-input v-model="form.name" @change="onInputChanged('name')" name="Name" />
          <label for="Title">Title</label>
          <b-form-input v-model="form.title" @change="onInputChanged('title')"
                        id="Title" name="Title" />
          <div class="">
            <label for="external">Internal or External?</label>
            <b-form-radio v-model="form.external" name="some-radios"
            value="1" @change="onInputChanged('external')">External</b-form-radio>
            <b-form-radio v-model="form.external" name="some-radios"
            value="0" @change="onInputChanged('external')">Internal</b-form-radio>
          </div>
          <label for="qty">Number people who fit this persona</label>
          <b-form-input type="number" v-model="form.market_size"
                id="qty" name="qty" @change="onInputChanged('market_size')"/>
          <label for="quote">Persona Quote</label>
          <b-form-textarea v-model="form.quote" id="quote"
                name="quote" @change="onInputChanged('quote')"/>
          <label for="function">Job Function</label>
          <b-form-textarea v-model="form.job_function" id="function"
                name="function" @change="onInputChanged('job_function')"/>
          <label for="needs">Needs</label>
          <b-form-textarea v-model="form.needs" id="needs"
                name="needs" @change="onInputChanged('needs')"/>
          <label for="wants">Wants</label>
          <b-form-textarea v-model="form.wants" id="wants"
                name="wants" @change="onInputChanged('wants')"/>
          <label for="pain-point">Pain Points</label>
          <b-form-textarea v-model="form.pain_point" id="pain_point"
                name="pain_point" @change="onInputChanged('pain_points')"/>
          <label for="buss-val">value to business</label>
          <b-form-input type="range" min="0" max="5" v-model="form.buss_val"
              @change="onInputChanged('buss_val')"/>
          <div class="mt-2">Value: {{ form.buss_val }}</div>
          <br>
          <label for="product-select">Add Product:    </label>
          <br>
          <multiselect
                      v-model="form.products" :options="product_options"
                      :multiple="true" :close-on-select="false"
                      :clear-on-select="false" :preserve-search="true"
                      placeholder="Pick some" label="product_name"
                      track-by="product_id" :preselect-first="false"
                      @input="onInputChanged('products')">
            <template slot="selection"
                      slot-scope="{ values, search, isOpen }">
              <span class="multiselect__single"
                    v-if="values.length &amp;&amp; !isOpen">
                          {{ values.length}} options selected
                        </span>
            </template>
          </multiselect>
          <br>
          <br>
          <multiselect
                      v-model="form.roles" :options="role_options"
                      :multiple="true" :close-on-select="false"
                      :clear-on-select="false" :preserve-search="true"
                      placeholder="Pick some" label="persona_role_name"
                      track-by="persona_role_id" :preselect-first="false"
                      @input="onInputChanged('roles')">
            <template slot="selection"
                      slot-scope="{ values, search, isOpen }">
              <span class="multiselect__single"
                    v-if="values.length &amp;&amp; !isOpen">
                          {{ values.length}} options selected
                        </span>
            </template>
          </multiselect>
          <br>
        </div>
        <div>
          <label for="persona_file">Add File</label>
          <b-form-file v-model="form.persona_file"
          :state="Boolean(form.persona_file)"
          name="persona_file"
          placeholder="Choose a file or drop it here..."
          drop-placeholder="Drop file here..."></b-form-file>
        </div>
        <div id="button-if" v-if='form.id != null'>
          <b-button type="reset" variant="secondary">Return</b-button>
          <b-button href="javascript:void(0)"
            type="button" variant="danger"  v-on:click='onArchive'> Archive</b-button>
          <b-button href="javascript:void(0)"
            type="submit" variant="primary" v-on:click='onEdit'>Submit Changes</b-button>
        </div>
        <div class="" v-else>
          <b-button type="button" variant="primary" v-on:click='onAdd'>Add New Persona</b-button>
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
import store from  "../../store";


export default {
  name: "persona-details",
  components : {'comment-view': CommentView },
  data() {
    return {
      form: {
        id : null,
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
        products: [],
        roles: [] ,
        persona_picture: '',
        persona_file: null},
      editing: false,
      source: 'persona',
      product_options: [],
      role_options: [],
      edited_fields: []
      }
    },
    beforeMount() {
      const self = this;

      // SET OPTIONS
      axios.get("/api/persona/roles")
        .then(response => {
          self.role_options = response.data;
        })
        .catch(error => console.log(error))

      axios.get("/api/products")
        .then(response => {
          self.product_options = response.data;
        })
        .catch(error => console.log(error))



      // UPDATE DATA ON CHANGES
      EventBus.$on('persona-selection-changed', function(selection){

        var get_url = "/api/persona-table/";
        get_url += selection;

        axios.get(get_url)
        .then(response => {
            self.form.id = selection;
            self.form.name = response.data[0].name;
            self.form.title= response.data[0].title;
            self.form.external= response.data[0].external;
            self.form.market_size= response.data[0].market_size;
            self.form.quote = response.data[0].quote;
            self.form.job_function = response.data[0].job_function;
            self.form.needs = response.data[0].needs;
            self.form.wants = response.data[0].wants;
            self.form.pain_point= response.data[0].pain_point;
            self.form.buss_val= response.data[0].buss_val;
            self.form.revision= response.data[0].revision;
            self.form.products = response.data[0].products;
            self.form.roles = response.data[0].roles;
            self.editing = false;
            self.edited_fields.length = 0 ;
          }
        )
        .catch(error => console.log(error))
        });
      },
      methods: {

      onInputChanged(field) {
        this.edited_fields.indexOf(field) === -1 ? this.edited_fields.push(field) :
        console.log(this.edited_fields)
      },

       async onEdit() {
         var key;
         var success = 1 ;
         for (key of this.edited_fields) {
           if (key === 'products') {
             await axios({
                 method: 'post',
                 url: '/api/persona-product',
                 data: this.form,
                 params : {
                   table : "persona"
                   }
                 })
                 .then(function (response) {
                   success = 1 * success ;})
           }
           else if (key === 'roles') {
             await axios({
                 method: 'post',
                 url: '/api/persona/roles',
                 data: this.form,
                 })
                 .then(function (response) {
                   success = 1 * success ;})
           }
           else {
             await axios({
                 method: 'put',
                 url: '/api/persona-table/' + this.form.id ,
                 data: {
                   'id' : this.form.id,
                    [key] : this.form[key]
                 }
                 })
                 .then(function (response) {
                   success = 1 * success ;})
               };
           }

        EventBus.$emit('persona-table-changed','item-updated');
        document.getElementById("right-sidepanel").style.width = "0px";
       },

       async onAdd() {
         await axios({
             method: 'post',
             url: '/api/persona-table',
             data: this.form, })
         .then(function (response) {
             console.log(response);})
         .catch(function (error) {
             console.log(error);})

        if (this.edited_fields.includes('products')) {
               await axios({
                   method: 'post',
                   url: '/api/persona-product',
                   data: this.form,
                   params : {
                     table : "persona"
                     }
                   })
         };

         EventBus.$emit('persona-table-changed','item-updated');
         document.getElementById("right-sidepanel").style.width = "0px";
       },

       onReset() {
         // Reset our form values
         this.editing = false;
       },

       async onArchive() {
         var get_url = '/api/persona-table/';
         get_url += this.form.id ;

         var archive_set = { 'archived': 1};

         console.log(get_url)
         await axios({
             method: 'PUT',
             url: get_url,
             data: archive_set,
             params: {
                table: "persona"
              }
            })
         .then(function (response) {
             console.log(response);})
         .catch(function (error) {
             console.log(error);})

         console.log('delete')
         EventBus.$emit('persona-table-changed' , archive_set )
         document.getElementById("right-sidepanel").style.width = "0px";
      },
     },
  };

</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>


<style scoped>

.avatar {
  vertical-align: middle;
  text-align: center;
  width: 100px;
  height: 100px;
  border-radius: 50%;
}

p {
  white-space: pre-line;
}

</style>
