
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
        <div v-if="form.job_function !== null">
          <label for="function">Job Function</label>
          <p class="text-wrap"> {{form.job_function}} </p>
        </div>
        <div v-if="form.needs !== null">
          <label for="needs" style="white-space: pre-line;">Needs</label>
          <p> {{form.needs}} </p>
        </div>
        <div v-if="form.wants !== null">
          <label for="wants" style="white-space: pre-line;">Wants</label>
          <p> {{form.wants}} </p>
        </div>
        <div v-if="form.pain_point !== null">
          <label for="pain_point">Pain Points</label>
          <p> {{form.pain_point}} </p>
        </div>
        <label for="buss_val">Market Value</label>
        <div class="barcont">
          <div class="bar buss_val"
          :style="{width:form.buss_val / 5 *100 + '%'}">{{form.buss_val}}</div>
        </div>
        <br>
        <label>Associated Products:</label>
        <div v-for="product in form.products" v-bind:key="product.id">
          <b-button :to='"/product/" +product.id' pill variant="info">{{product.name}}</b-button>
          <!-- TODO: make it so clicking her routes to the product -->
        </div>
        <br>
        <label>Associated Roles:</label>
        <div v-for="role in form.roles" v-bind:key="role.id">
          <b-badge pill variant="success">{{role.name}}</b-badge>
        </div>
        <br>
        <label>Files:</label>
        <div v-for="uploadedFile in uploadedFiles" v-bind:key="uploadedFile.id">
          {{uploadedFile.filename}}
          <button
            type="button" name="button" target="_blank" v-on:click="getFile(uploadedFile.id)">
            <i class="fa fa-file"></i>
          </button>
        </div>
        <hr>

      </div>
      <b-button href="javascript:void(0)" v-on:click="editing = true">Edit</b-button>
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
<!--            THERE ARE SOME COMPLEX INTERACTIONS GOING ON HERE NEED TO CONSIDER FURTHER
          <div variant="light" v-b-toggle="'collapse-needs'" class="m-1">
                  <label for="needs">Needs</label>
          </div>
                <b-collapse id="collapse-needs">
                  <b-form-textarea v-model="form.needs" id="needs"
                        name="needs" @change="onInputChanged('needs')"/>
                </b-collapse> -->

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
                      placeholder="Pick some" label="name"
                      track-by="id" :preselect-first="false"
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
                      placeholder="Pick some" label="name"
                      track-by="id" :preselect-first="false"
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
        <!-- Single file -->
        <br>
        <b-form-file
          type="file" id="file" ref="file"
          v-model="file"
          :state="Boolean(file)"
          placeholder="Choose a file or drop it here..."
          drop-placeholder="Drop file here...">
        </b-form-file>
        <b-button variant="info"
          href="javascript:void(0)" v-on:click='submitFiles()'>Upload</b-button>
        <br>
        <div v-for="uploadedFile in uploadedFiles" v-bind:key="uploadedFile.id">
          {{uploadedFile.filename}}
          <b-button variant="outline-primary"
            type="button" href="javascript:void(0)" v-on:click="getFile(uploadedFile.id)">
            <i class="fa fa-file"></i>
          </b-button>
          <b-button variant="outline-primary" v-on:click="deleteFile(uploadedFile.id)"
              type="button" href="javascript:void(0)">&times;
          </b-button>
        </div>
        <hr>

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

      <br>
      <div class="right" style="align-content:right">
        <span>add to playlist -> </span>
        <playlist-add class="right" :key='form.id' :source='"persona"' :source_id="form.id"/>
      </div>
      <h4>Comments</h4>
      <comment-view v-if='form.id != null'
                    :key='form.id'
                    v-bind:sourceTable="source"
                    v-bind:itemId='form.id'>
      </comment-view>

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
        name: null,
        title: null,
        external: null,
        market_size: null,
        quote: null,
        job_function: null,
        needs: null,
        wants: null,
        pain_point: null,
        buss_val: null,
        revision: null,
        products: [],
        roles: [] ,
        persona_picture: null,
        persona_file: null},
      uploadedFiles: [],
      file: null,
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

          //GET FILES
          axios({
            method: 'get',
            url: '/api/persona/files/' + selection,
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
                 url: '/api/persona-table/' + this.form.id ,
                 data: {
                    [key] : this.form[key]
                    }
                 })
           };

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

         EventBus.$emit('persona-table-changed','item-added');
         document.getElementById("right-sidepanel").style.width = "0px";
       },

       onReset() {
         // Reset our form values
         this.editing = false;
       },

       async onArchive() {
         var get_url = '/api/persona-table/';
         get_url += this.form.id ;


         console.log(get_url)
         await axios({
             method: 'PUT',
             url: get_url,
             data: { 'archived': true},
            })
         .then(function (response) {
             console.log(response);})
         .catch(function (error) {
             console.log(error);})

         console.log('delete')
         EventBus.$emit('persona-table-changed' , "archived" )
         document.getElementById("right-sidepanel").style.width = "0px";
      },

      getFile(file_id) {
          const self = this;
          axios({
          method: 'get',
          url: '/api/persona/files/'+this.form.id+'?file_id='+ file_id
        }
        ).then(function(response){
          var fileURL = window.URL.createObjectURL(new Blob([response.data]));
          var fileLink = document.createElement('a');

          fileLink.href = fileURL;
          fileLink.setAttribute('download');
          document.body.appendChild(fileLink);

          fileLink.click();
          console.log(response);
        })
      },

      handleFileUpload(){
        this.file = this.$refs.file.files[0];
      },

      submitFiles(){

              let formData = new FormData();

              formData.append('file', this.file);
              formData.append('filename', 'blank');

              axios({
                method: 'post',
                url: '/api/persona/files/' + this.form.id,
                data : formData,
                headers: {
                      'Content-Type': 'multipart/form-data'
                }
              }
              ).then(function(response){
                console.log(response);
              })
              .catch(function(error){
                console.log(error);
              });
      },

      deleteFile(){
        const self = this;
        axios({
          method: 'delete',
          url: '/api/persona/files/'+this.form.id+'?file_id='+ file_id
        })
        // need to add action to update view
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

.barcont {
  width: 100%; /* Full width */
  background-color: #ddd; /* Grey background */
  height: 20px;
}

.bar {
    text-align: right; /* Right-align text */
    vertical-align: center;
    color: white; /* White text color */
    height: 20px;
}

.bar.buss_val {
    width: 65%;
    background-color: #4CAF50;
}

p {
  white-space: pre-line;
}

</style>
