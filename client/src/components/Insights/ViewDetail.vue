
<template>
<div style="padding-right:15px; margin-left:15px">
  <!-- <div role="tablist">
          <b-button block href="#" v-b-toggle.accordion-1
          variant="btn-outline-secondary">Wants</b-button>
        <b-collapse id="accordion-1" accordion="my-accordion" >
          <b-form-textarea v-model="form.wants" id="quote" name="quote" />
        </b-collapse>

          <b-button block href="#" v-b-toggle.accordion-2
          variant="btn-outline-secondary">Quote</b-button>
        <b-collapse id="accordion-2" accordion="my-accordion" >
          <b-form-textarea v-model="form.quote" id="quote" name="quote" />
        </b-collapse>

          <b-button block href="#" v-b-click.accordion-3
          variant="btn-outline-secondary">Accordion 3</b-button>
        <b-collapse id="accordion-3" v-model="visible" tag="link">
            <div>{{ form.quote }}</div>
        </b-collapse>
    </div> -->
<!--

break
break

 -->

    <b-form id='persona-detail'
        @submit="onEdit"
        @reset="onReset"
        @archive="onArchive">
      <div id='persona-detail-show' v-if='editing === false && form.id !== null'>
      <h1>Insight Detail</h1>
      <div class="">>
        <label>Title</label>
        <p class="text-wrap"> {{form.title}} </p>
        <label>description</label>
        <p class="text-wrap"> {{form.description}} </p>
        <label>content</label>
        <p class="text-wrap"> {{form.content}} </p>
        <label>Experience vector</label>
        <p class="text-wrap"> {{form.experience_vector}} </p>
        <label>Magnitude</label>
        <p class="text-wrap"> {{form.magnitude}} </p>
        <label>Frequency</label>
        <p class="text-wrap"> {{form.frequency}} </p>
        <label>Emotions</label>
        <p class="text-wrap"> {{form.emotions}} </p>
        <label>Props</label>
        <p class="text-wrap"> {{form.props}} </p>
        <label>Journey Location</label>
        <p class="text-wrap"> {{form.journey}} </p>
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

          <label>Title</label>
          <b-form-input v-model="form.title" @change="onInputChanged('title')"
                        id="Title" name="Title" />
          <label>description</label>
          <b-form-textarea v-model="form.description" id="description"
                name="description" @change="onInputChanged('description')"/>
          <label>content</label>
          <b-form-textarea v-model="form.content" id="content"
                name="content" @change="onInputChanged('content')"/>
          <label>Experience vector</label>
          <b-form-textarea v-model="form.experience_vector" id="experience_vector"
                name="experience_vector" @change="onInputChanged('experience_vector')"/>
          <label>Magnitude</label>
          <b-form-textarea v-model="form.magnitude" id="magnitude"
                name="magnitude" @change="onInputChanged('magnitude')"/>
          <label>Frequency</label>
          <b-form-textarea v-model="form.frequency" id="frequency"
                name="frequency" @change="onInputChanged('frequency')"/>
          <label>Emotions</label>
          <b-form-textarea v-model="form.emotions" id="emotions"
                name="emotions" @change="onInputChanged('emotions')"/>
          <label>Props</label>
          <b-form-textarea v-model="form.props" id="props"
                name="props" @change="onInputChanged('props')"/>
          <label>Journey Location</label>
          <b-form-textarea v-model="form.journey" id="journey"
                name="journey" @change="onInputChanged('journey')"/>
          <br>
          <label for="product-select">Add Product:    </label>
          <br>
          <multiselect
                      @change="onInputChanged('products')"
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
        experience_vector: '',
        magnitude: '',
        frequency: '',
        emotions: '',
        props: '',
        journey: '',
        creator_id: '',
        revision: '',
        products: [],
        personas: []
      },
      editing: false,
      source: 'insights',
      product_options: [],
      persona_options: [],
      edited_fields: [],
      }
    },
    beforeMount() {
      const self = this;

      // SET OPTIONS
      axios.get("/api/products")
        .then(response => {
          self.product_options = response.data;
        })
        .catch(error => console.log(error))

      // UPDATE DATA ON CHANGES
      EventBus.$on('insight-selection-changed', function(selection){

        var get_url = "/api/insights/";
        get_url += selection;

        axios.get(get_url)
        .then(response => {
            self.form.id = selection;
            self.form.title= response.data[0].title;
            self.form.description= response.data[0].description;
            self.form.experience_vector= response.data[0].experience_vector;
            self.form.magnitude = response.data[0].magnitude;
            self.form.frequency= response.data[0].frequency;
            self.form.emotions = response.data[0].emotions;
            self.form.props = response.data[0].props;
            self.form.journey= response.data[0].journey;
            self.form.personas= response.data[0].personas;
            self.form.products = response.data[0].product;
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

      changeData() {
        EventBus.$emit('data-changed',this.form.id)
        console.log('send')
      },

      ///                 }

       onEdit() {
         var key;
         for (key of this.edited_fields) {
           axios({
               method: 'put',
               url: '/api/insights/' + this.form.id ,
               data: {
                 'id' : this.form.id,
                  [key] : this.form[key]
               }
               })
             };

        if (this.edited_fields.match('products')) {
          axios({
              method: 'post',
              url: '/api/insights',
              data: this.form,
              params : {
                table : "persona"
                }
              })
        };

        EventBus.$emit('insight-table-changed','item-updated');
        document.getElementById("right-sidepanel").style.width = "0px";

       },

       onAdd() {
         axios({
             method: 'post',
             url: '/api/insights',
             data: this.form, })
         .then(function (response) {
             console.log(response);})
         .catch(function (error) {
             console.log(error);})

        if (this.edited_fields.match('products')) {
               axios({
                   method: 'post',
                   url: '/api/insights',
                   data: this.form,
                   params : {
                     table : "persona"
                     }
                   })
         };

         EventBus.$emit('insight-table-changed','item-updated');
         document.getElementById("right-sidepanel").style.width = "0px";
       },

       onReset() {
         // Reset our form values
         this.editing = false;
       },

       onArchive() {
         var get_url = '/api/insights/';
         get_url += this.form.id ;

         var archive_set = { 'archived': 1};

         console.log(get_url)
         axios({
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
         EventBus.$emit('insight-table-changed' , archive_set )
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
