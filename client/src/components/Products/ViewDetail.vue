
<template>
<div style="padding-right:15px; margin-left:15px">
  <b-form id='product-detail'
        @submit.prevent="onEdit"
        @reset="onReset"
        @archive="onArchive">
      <div id='product-detail-show' v-if='editing === false && form.id !== null'>
        <h1>Detail</h1>
        <span> Product ID: {{form.id}} | Revision: {{form.revision}}  </span>
        <div>
          <label>Name</label>
          <p class="text-wrap"> {{form.name}} </p>
          <label>Description</label>
          <p class="text-wrap"> {{form.description}} </p>
          <div v-if="form.metrics!== null">
            <label>Metrics</label>
            <p class="text-wrap"> {{form.metrics}} </p>
          </div>
          <div v-if="form.features!== null">
            <label>Product Features</label>
            <p class="text-wrap"> {{form.features}} </p>
          </div>
          <div v-if="form.goals!== null">
            <label>Goals</label>
            <p class="text-wrap"> {{form.goals}} </p>
          </div>
          <label for="function">Owner</label>
          <p class="text-wrap"> {{form.owner}} </p>
          <label>Product Homepage</label>
          <p> {{form.product_homepage}} </p>
          <br>
          <b-form-group label="Product Life stage">
            <b-form-radio-group
              disabled
              id="radio-group-1"
              v-model="form.product_life"
              :options="product_life_options"
              name="radio-options" />
          </b-form-group>
          <label>Personas: </label><br>
          <div style="display:inline-block;"
               v-for="persona in form.personas"
               v-bind:key="persona.id">
            <b-button :to='"/persona/" +persona.id' pill variant="info" size="sm">
              {{persona.title}} </b-button>
          </div>
        </div>
        <label>Files:</label>
        <div v-for="uploadedFile in uploadedFiles" v-bind:key="uploadedFile.id">
          {{uploadedFile.filename}}
          <b-button
            type="button" name="button" target="_blank"
            :href ="'/api/product/files/' + form.id + '?file_id=' + uploadedFile.id"
            download>
            <i class="fa fa-file"></i>
          </b-button>
        </div>
        <hr>
        <b-button
            href="javascript:void(0)"
            v-if="this.$store.getters.isLoggedIn"
            v-on:click="editing = true">
            Edit
        </b-button>
      </div>
      <div  id='product-detail-edit' v-else>
        <h1 v-if='form.id !== null'>Edit</h1>
        <h1 v-else>Add</h1>
        <div>
          <label>Name</label>
          <b-form-input v-model="form.name"
              @change="onInputChanged('name')"></b-form-input>
          <label>Description</label>
          <b-form-textarea v-model="form.description"
              @change="onInputChanged('description')"></b-form-textarea>
          <label>Metrics</label>
          <b-form-textarea v-model="form.metrics"
              @change="onInputChanged('metrics')"></b-form-textarea>
          <label>Product Features</label>
          <b-form-textarea v-model="form.features"
              @change="onInputChanged('features')"></b-form-textarea>
          <label>Goals</label>
          <b-form-input v-model="form.goals"
              @change="onInputChanged('goals')"></b-form-input>
          <label for="function">Owner</label>
          <b-form-input v-model="form.owner"
              @change="onInputChanged('owner')"></b-form-input>
          <label>Product Homepage</label>
          <b-form-input v-model="form.product_homepage"
              @change="onInputChanged('product_homepage')"></b-form-input>
          <br>

          <label>Product Life Stage</label>
          <b-form-group label="Life stage" >
            <b-form-radio-group
              @change="onInputChanged('product_life')"
              id="radio-group-1"
              v-model="form.product_life"
              :options="product_life_options"
              name="radio-options" />
          </b-form-group>

          <label>Choose Personas</label>
          <multiselect
                      @change="onInputChanged('personas')"
                      v-model="form.personas" :options="persona_options"
                      :multiple="true" :close-on-select="false"
                      :clear-on-select="false" :preserve-search="true"
                      placeholder="Pick some" label="title"
                      track-by="id" :preselect-first="false">
            <template slot="selection"
                      slot-scope="{ values, search, isOpen }">
              <span class="multiselect__single"
                    v-if="values.length &amp;&amp; !isOpen">
                          {{ values.length}} options selected
                        </span>
            </template>
          </multiselect>
          <br>
          <div >Selected: <strong>{{form.personas.title}}</strong></div>
        </div>
        <!-- Single file -->
        <br>
        <div class="wrapper" v-if='form.id != null'>
          <label>Files</label>
          <!-- v-on:change="handleFilesUpload()" -->
          <b-form-file
            type="file" id="file" ref="file"
            v-model="file"
            :state="Boolean(file)"
            placeholder="Choose a file or drop it here..."
            drop-placeholder="Drop file here...">
          </b-form-file>
          <b-button variant="info" id='file-upload'
            href="javascript:void(0)" v-on:click='submitFiles()'>Upload</b-button>
          <br>
          <div v-for="uploadedFile in uploadedFiles" v-bind:key="uploadedFile.id">
            {{uploadedFile.filename}}
            <b-button
                  variant="outline-primary"
                  type="button"
                  :href ="'/api/product/files/' + form.id + '?file_id=' + uploadedFile.id"
                  download>
              <i class="fa fa-file"></i>
            </b-button>
            <b-button variant="outline-primary" v-on:click="deleteFile(uploadedFile.id)"
                type="button" href="javascript:void(0)">&times;
            </b-button>
          </div>
        </div>

        <br>
        <div id="button-if" v-if='form.id != null'>
            <b-button type="reset" variant="secondary">Return</b-button>
            <b-button href="javascript:void(0)"
              type="button" variant="danger"  v-on:click='onArchive'> Archive</b-button>
            <b-button href="javascript:void(0)"
              type="submit" variant="primary" v-on:click='onEdit'>Submit Changes</b-button>
        </div>
        <div v-else>
            <b-button type="submit" variant="primary" v-on:click='onAdd'>
              Add New Product</b-button>
        </div>
      </div>
  </b-form>

  <hr>
    <playlist-add
          :style="{right:30+'px' , position: 'absolute'}"
          :key="form.id"
          id="tooltip-target-1"
          class="right"
          :source='"product"'
          :source_id="form.id"/>

  <h4>Comments</h4>
  <comment-view v-if='form.id != null'
                :key='form.id'
                v-bind:sourceTable="source"
                v-bind:itemId='form.id'>
  </comment-view>
  <br>
</div>
</template>

<script>
/*eslint-disable */
import axios from 'axios'
import CommentView from '../CommentView.vue'
import {EventBus} from "../../index.js";
import store from  "../../store";
import api from '../../api'

export default {
  name: "product-details",
  components : {'comment-view': CommentView },
  data() {
    return {
      form: {
        id: null,
        name: null,
        description: null,
        metrics: null,
        features: null,
        goals: null,
        owner: '',
        product_homepage: '',
        personas: [],
        products:[],
        product_photo: '',
        product_life: null,
        product_file: null},
      uploadedFiles: [],
      file: null,
      errors: {},
      editing: false,
      source: 'product',
      edited_fields: [],
      product_life_options: ['POC','MVP','G2M','Maturing','Declining']
      }
    },
    computed: {
      persona_options(){
        return store.state.personas
      },
    },
    beforeMount() {
      const self = this;

      // GET ON DATA CHANGE
      EventBus.$on('product-selection-changed', async function(selection){

        const {data} = await api.productTableById(selection);

        self.form.id = data[0].id;
        self.form.name = data[0].name;
        self.form.description= data[0].description;
        self.form.metrics= data[0].metrics;
        self.form.goals= data[0].goals;
        self.form.features = data[0].features;
        self.form.owner = data[0].owner;
        self.form.product_homepage = data[0].product_homepage;
        self.form.product_life = data[0].product_life;
        self.form.revision = data[0].revision;
        self.form.personas = data[0].personas;
        self.editing = false;
        self.edited_fields.length = 0 ;


        //GET FILES
        var response
        response = await api.productFilesById(selection);
        self.uploadedFiles = response.data;

        });

      },
      methods: {
        onInputChanged(field) {
          this.edited_fields.indexOf(field) === -1 ? this.edited_fields.push(field) :
          console.log(this.edited_fields)
        },

        async onEdit() {
          var key;
          for (key of this.edited_fields) {
            const data = {[key] : this.form[key]}
            await api.productTablePutById(this.form.id,data)
                };

         EventBus.$emit('product-changed','item-updated');
         document.getElementById("right-sidepanel").style.width = "0px";
         this.$store.commit({
           type: 'alert',
           show : 2,           //seconds to auto dismiss
           variant : "success",
           content : "product updated"
         })
        },

       async onAdd(evt) {
         evt.preventDefault()
         const data = this.form
         await api.productPost(data)

         EventBus.$emit('product-changed','item-updated');
         document.getElementById("right-sidepanel").style.width = "0px";
         this.$store.commit({
           type: 'alert',
           show : 2,           //seconds to auto dismiss
           variant : "success",
           content : "product created!"
         })
       },

       onReset(evt) {
         evt.preventDefault()
         // Reset our form values
         this.editing = false;
       },

       async onArchive(evt) {
         evt.preventDefault()
         await axios({
            method: 'put',
            url: '/api/product/' + this.form.id ,
         })
         .then(function (response) {
             console.log(response);})
         .catch(function (error) {
             console.log(error);})

         EventBus.$emit('product-changed' , 'archived' )
         document.getElementById("right-sidepanel").style.width = "0px";
         this.$store.commit({
           type: 'alert',
           show : 3,           //seconds to auto dismiss
           variant : "warning",
           content : "product archived, NOTE: data is not deleted, if this was done unintentially please reach out to the admin"
         })
      },

      submitFiles(){
        api.putProductFilesById(this.form.id,this.file)
      },

      deleteFile(file_id){
        api.deleteProductFilesById(this.form.id)
        // need to add action to update view
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
}

p {
  white-space: pre-line;
}

</style>
