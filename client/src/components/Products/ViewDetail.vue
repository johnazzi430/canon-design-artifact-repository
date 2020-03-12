
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
        <b-button href="javascript:void(0)" v-on:click="editing = true">Edit</b-button>
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
      persona_options : [],
      edited_fields: [],
      product_life_options: ['POC','MVP','G2M','Maturing','Declining']
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
      EventBus.$on('product-selection-changed', function(selection){

        var get_url = "/api/product/";
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
            self.form.product_life = response.data[0].product_life;
            self.form.revision = response.data[0].revision;
            self.form.personas = response.data[0].personas;
            self.editing = false;
            self.edited_fields.length = 0 ;
          }
        )
        .catch(error => console.log(error))

        //GET FILES
        axios({
            method: 'get',
            url: '/api/product/files/' + selection,
          }).then(function(response){
            self.uploadedFiles = response.data;
          })

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
             await axios({
                  method: 'put',
                  url: '/api/product/' + this.form.id ,
                  data: {
                     [key] : this.form[key]
                   }
                  })
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
         await axios({
             method: 'post',
             url: '/api/product',
             data: this.form, })
         .then(function (response) {
             console.log(response);})
         .catch(function (error) {
             console.log(error);})

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
              let formData = new FormData();

              document.getElementById('file-upload').innerHTML = '<b-spinner label="Loading..."></b-spinner>';

              formData.append('file', this.file);
              formData.append('filename', 'blank');

              axios({
                method: 'post',
                url: '/api/product/files/' + this.form.id,
                data : formData,
                headers: {
                      'Content-Type': 'multipart/form-data'
                }
              }).then(function(response){
                document.getElementById('file-upload').innerHTML = '<i class="fa fa-check"></i>';
                console.log('file uploaded')
              })
              .catch(function(error){
                document.getElementById('file-upload').innerHTML = '<i class="fa fa-times nav-icon"></i>';
                console.log('upload error')
              });
      },

      deleteFile(file_id){
        const self = this;
        axios({
          method: 'delete',
          url: '/api/product/files/'+this.form.id+'?file_id='+ file_id
        })
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
