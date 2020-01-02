
<template>
<div style="padding-right:15px; margin-left:15px">

    <b-form id='persona-detail'
        @submit="onEdit"
        @reset="onReset"
        @archive="onArchive">
      <div id='persona-detail-show' v-if='editing === false && form.id !== null'>
      <h1>Insight Detail</h1>
      <div class="">
        <label>Title</label>
        <p class="text-wrap"> {{form.title}} </p>
        <label>description</label>
        <p class="text-wrap"> {{form.description}} </p>
        <label>Content</label>
        <p class="text-wrap"> {{form.content}} </p>
        <label>Experience vector</label>
        <br>
        <span class="badge badge-pill badge-success"
          v-bind:class="form.experience_vector">
          {{form.experience_vector}}</span>
          <br>
        <label>Magnitude</label>
        <div class="barcont">
          <div class="bar magnitude"
          :style="{width:form.magnitude/ 5 *100 + '%'}">{{form.magnitude}}</div>
        </div>
        <label>Frequency</label>
        <div class="barcont">
          <div class="bar frequency"
          :style="{width:form.frequency/ 5 *100 + '%'}">{{form.frequency}}</div>
        </div>
        <label>Emotions</label>
        <p class="text-wrap"> {{form.emotions}} </p>
        <label>Props</label>
        <p class="text-wrap"> {{form.props}} </p>
        <label>Journey Location</label>
        <p class="text-wrap"> {{form.journey}} </p>
        <label>Associated Personas</label>
        <div v-for="persona in form.personas" v-bind:key="persona.id">
          <b-badge :to="{ path: 'persona/' + persona.id }" pill
          variant="success">{{persona.title}} </b-badge>
        </div>
        <br>
        <label>Associated products</label>
        <div v-for="product in form.products" v-bind:key="product.id">
          <b-badge :to="{ path: 'product/' + product.id }" pill
          variant="success">{{product.name}}</b-badge>
        </div>
      </div>
      <br>
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

          <label>Title</label>
          <b-form-input v-model="form.title" @change="onInputChanged('title')"
                        id="Title" name="Title" />
          <!-- Collapasble form input  -->
          <div variant="light" v-b-toggle="'collapse-description'" class="m-1">
            <label>description</label>
          </div>
          <b-collapse id="collapse-description">
            <b-form-input v-model="form.description" id="description"
            name="description" @change="onInputChanged('description')"/>
          </b-collapse>

          <label>content</label>
          <b-form-textarea v-model="form.content" id="content"
                name="content" @change="onInputChanged('content')"/>
          <label>Experience vector</label>
          <b-form-select :options="experience_options"
                v-model="form.experience_vector" id="experience_vector"
                name="experience_vector" @change="onInputChanged('experience_vector')"/>
          <label>Magnitude: {{form.magnitude}}</label>
          <b-form-input type="range" min="0" max="5" v-model="form.magnitude" id="magnitude"
                name="magnitude" @change="onInputChanged('magnitude')"/>
          <label>Frequency: {{form.frequency}}</label>
          <b-form-input type="range" min="0" max="5" v-model="form.frequency" id="frequency"
                name="frequency" @change="onInputChanged('frequency')"/>
          <label>Emotions</label>
          <b-form-select v-model="form.emotions" id="emotions" :options='emotion_options'
                name="emotions" @change="onInputChanged('emotions')"/>
          <label>Props</label>
          <b-form-textarea v-model="form.props" id="props"
                name="props" @change="onInputChanged('props')"/>
          <label>Journey Location</label>
          <b-form-select v-model="form.journey" id="journey" :options="journey_options"
          name="journey" @change="onInputChanged('journey')"/>

          <div class="large-12 medium-12 small-12 cell">
            <label>Files
              <input type="file" id="files" ref="files" multiple v-on:change="handleFilesUpload()"/>
            </label>
            <button href="javascript:void(0)" v-on:click="submitFiles()">Submit</button>
          </div>
          <br>
          <label for="persona-select">Choose Personas: </label>
          <br>
          <multiselect
                      @input="onInputChanged('personas')"
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
          <label for="product-select">Product:    </label>
          <br>
          <label>Choose Products</label>
          <multiselect
                      @input="onInputChanged('products')"
                      v-model="form.products" :options="product_options"
                      :multiple="true" :close-on-select="false"
                      :clear-on-select="false" :preserve-search="true"
                      placeholder="Pick some" label="product_name"
                      track-by="product_id" :preselect-first="false">
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
          <label for="file">Add File</label>
          <b-form-file v-model="form.file"
          :state="Boolean(form.file)"
          name="file"
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
  name: "insight-details",
  components : {'comment-view': CommentView },
  data() {
    return {
      form: {
        id : null,
        title: '',
        description: '',
        content: '',
        file: null,
        experience_vector: 'Neutral',
        magnitude: null,
        frequency: null,
        emotions: null,
        props: '',
        journey: '',
        creator_id: null,
        revision: null,
        products: [],
        personas: []
      },
      editing: false,
      source: 'insights',
      experience_options: ["Positive", "Neutral", "Negative"],
      emotion_options: ["Pain", "Joyful", "Triumphiant", "Angry", "Calm", "Frustrated", "Surprised" , "Excited"],
      journey_options: ["Aware", "Try", "Use", "Leave"],
      product_options: [],
      persona_options: [],
      edited_fields: [],
      }
    },
    beforeMount() {
      const self = this;

      // SET OPTIONS
      axios.get("/api/products")
        .then(response => {self.product_options = response.data;})

      axios.get("/api/personas")
        .then(response => {self.persona_options = response.data;})

      // UPDATE DATA ON CHANGES
      EventBus.$on('insight-selection-changed', function(selection){

        //make sure when "add" button is pressed no errors are thrown
        if (selection === null) {
          return
        }

        var get_url = "/api/insights/";
        get_url += selection;

        axios.get(get_url)
        .then(response => {
            self.form.id = selection;
            self.form.title= response.data[0].title;
            self.form.description= response.data[0].description;
            self.form.content = response.data[0].content;
            self.form.experience_vector= response.data[0].experience_vector;
            self.form.magnitude = response.data[0].magnitude;
            self.form.frequency= response.data[0].frequency;
            self.form.emotions = response.data[0].emotions;
            self.form.props = response.data[0].props;
            self.form.journey= response.data[0].journey;
            self.form.personas = response.data[0].personas;
            self.form.products = response.data[0].products;
            self.editing = false;
            self.edited_fields.length = 0 ;
          }
        )
        .catch(error => console.log(error))

        });
      },
      methods: {

      onInputChanged(field) {
        // add list of edited fields to array to reduce api calls on backend
        this.edited_fields.indexOf(field) === -1 ? this.edited_fields.push(field):
        console.log(this.edited_fields)
      },

      submitFiles(){

              let formData = new FormData();

              for( var i = 0; i < this.files.length; i++ ){
                let file = this.files[i];

                formData.append('files[' + i + ']', file);
              }

              axios.post( '/api/insights/files',
                formData,
                {
                  headers: {
                      'Content-Type': 'multipart/form-data'
                  }
                }
              ).then(function(){
                console.log('SUCCESS!!');
              })
              .catch(function(){
                console.log('FAILURE!!');
              });
      },

      handleFilesUpload(){
        this.files = this.$refs.files.files;
      },

       async onEdit() {
         var key;
         for (key of this.edited_fields) {
           if (key.match('products')) {
             await axios({
                 method: 'post',
                 url: '/api/insights/'+ this.form.id +'/products',
                 data: this.form.products,
                 })
           }
           else if (key.match('personas')) {
             await axios({
                 method: 'post',
                 url: '/api/insights/'+ this.form.id +'/personas',
                 data: this.form.personas,
                 })
           }
           else {
           await axios({
               method: 'put',
               url: '/api/insights/' + this.form.id ,
               data: {
                 'id' : this.form.id
               }
               })
             };
           };

        EventBus.$emit('insight-data-changed','item-updated');
        document.getElementById("right-sidepanel").style.width = "0px";

       },

       async onAdd() {
         await axios({
             method: 'post',
             url: '/api/insights',
             data: this.form, })

        if (Array.isArray(this.edited_fields.length )) {
          if (this.edited_fields.match('products')) {
                 await axios({
                     method: 'post',
                     url: '/api/insights/'+ this.form.id +'/products',
                     data: this.form.products,
                     })
               }
          else if (this.edited_fields.match('personas')) {
                 await axios({
                     method: 'post',
                     url: '/api/insights/'+ this.form.id +'/personas',
                     data: this.form.personas,
                     })
          }
        }

         EventBus.$emit('insight-data-changed','item-updated');
         document.getElementById("right-sidepanel").style.width = "0px";
       },

       onReset() {
         // Reset our form values
         this.editing = false;
       },

       async onArchive() {
         var get_url = '/api/insights/';
         get_url += this.form.id ;

         var archive_set = { 'archived': 1};

         console.log(get_url)
         await axios({
             method: 'PUT',
             url: get_url,
             data: archive_set,
             params: {
                table: "insights"
              }
            })
         .then(function (response) {
             console.log(response);})
         .catch(function (error) {
             console.log(error);})

         console.log('delete')
         EventBus.$emit('insight-data-changed' , archive_set )
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

.badge.Negative{
  background-color: red
}

.badge.Positive{
  background-color: green
}

.badge.Neutral{
  background-color: grey
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

.bar.magnitude {
    background-color: #4CAF50;
}

.bar.frequency{
    background-color: #4CAF50;
}

</style>
