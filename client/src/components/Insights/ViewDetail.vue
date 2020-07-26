
<template>
<div style="padding-right:15px; margin-left:15px">

    <b-form id='persona-detail'
        @submit="onEdit"
        @reset="onReset"
        @archive="onArchive">
      <div id='persona-detail-show' v-if='editing === false && form.id !== null'>
        <!-- Show view -->
      <div class="">
        <h2>{{form.title}}</h2>
        <editor-content class="editor-box" :editor="editor" :editable="false"/>

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

        <label v-if="form.personas.length">Associated Personas</label>
        <div v-for="persona in form.personas" v-bind:key="persona.id + persona.title">
          <b-badge :to="{ path: 'persona/' + persona.id }" pill
          variant="success">{{persona.title}} </b-badge>
        </div>
        <br>
        <label v-if="form.products.length">Associated products</label><br>
        <div style="display:inline-block;"
             v-for="product in form.products"
             v-bind:key="product.id + product.name">
          <b-badge :to="{ path: 'product/' + product.id }" pill
          variant="success">{{product.name}}</b-badge>
        </div>
        <br>
        <label v-if="uploadedFiles.length">Files:</label><br>
        <div style="display:inline-block;"
             v-for="uploadedFile in uploadedFiles"
             v-bind:key="uploadedFile.id + uploadedFile.filename">
          {{uploadedFile.filename}}
          <b-button
            type="button" name="button" target="_blank"
            :href ="'/api/insights/files/' + form.id + '?file_id=' + uploadedFile.id"
            download>
            <i class="fa fa-file"></i>
          </b-button>
        </div>
      </div>
      <br>
      <b-button
          href="javascript:void(0)"
          v-if="this.$store.getters.isLoggedIn && this.form.archived === false"
          v-on:click="editing = true">
          Edit
      </b-button>

    </div>
      <div  id='persona-detail-edit' v-else>
        <!-- Edditing or Adding view -->
        <h2 v-if='form.id === null'>Add</h2>
        <h2 v-else>Edit</h2>
        <hr>
        <div>


          <b-form-input v-model="form.title" @change="onInputChanged('title')"
                          class="h2" id="Title" name="Title" placeholder="Title">
          </b-form-input>

          <editor-menu-bar :editor="editor" v-slot="{ commands, isActive, focused }">
            <div
              class="menubar is-hidden"
              :class="{ 'is-focused': focused }"
            >

              <button
                class="menubar__button"
                :class="{ 'is-active': isActive.bold() }"
                @click.prevent="commands.bold"
              >
                <i class="fa fa-bold" aria-hidden="true"></i>
              </button>

              <button
                class="menubar__button"
                :class="{ 'is-active': isActive.italic() }"
                @click.prevent="commands.italic"
              >
                <i class="fa fa-italic" aria-hidden="true"></i>
              </button>

              <button
                class="menubar__button"
                :class="{ 'is-active': isActive.strike() }"
                @click.prevent="commands.strike"
              >
                <i class="fa fa-strikethrough" aria-hidden="true"></i>
              </button>

              <button
                class="menubar__button"
                :class="{ 'is-active': isActive.underline() }"
                @click.prevent="commands.underline"
              >
                <i class="fa fa-underline" aria-hidden="true"></i>
              </button>

              <button
                class="menubar__button"
                :class="{ 'is-active': isActive.code() }"
                @click.prevent="commands.code"
              >
                <i class="fa fa-code" aria-hidden="true"></i>
              </button>

              <button
                class="menubar__button"
                :class="{ 'is-active': isActive.paragraph() }"
                @click.prevent="commands.paragraph"
              >
                <i class="fa fa-paragraph" aria-hidden="true"></i>
              </button>

              <button
                class="menubar__button"
                :class="{ 'is-active': isActive.heading({ level: 1 }) }"
                @click.prevent="commands.heading({ level: 1 })"
              >
                H1
              </button>

              <button
                class="menubar__button"
                :class="{ 'is-active': isActive.heading({ level: 2 }) }"
                @click.prevent="commands.heading({ level: 2 })"
              >
                H2
              </button>

              <button
                class="menubar__button"
                :class="{ 'is-active': isActive.heading({ level: 3 }) }"
                @click.prevent="commands.heading({ level: 3 })"
              >
                H3
              </button>

              <button
                class="menubar__button"
                :class="{ 'is-active': isActive.bullet_list() }"
                @click.prevent="commands.bullet_list"
              >
                <i class="fa fa-list" aria-hidden="true"></i>
              </button>

              <button
                class="menubar__button"
                :class="{ 'is-active': isActive.blockquote() }"
                @click.prevent="commands.blockquote"
              >
                <i class="fa fa-quote-left" aria-hidden="true"></i>
              </button>

              <button
                class="menubar__button"
                @click.prevent="commands.horizontal_rule"
              >
                <i class="fa fa-window-minimize" aria-hidden="true"></i>
              </button>

              <!-- <button
                class="menubar__button"
                @click.prevent="commands.createTable({
                                                     rowsCount: 3,
                                                     colsCount: 3,
                                                     withHeaderRow: false
                                                    })"
              >
                <i class="fa fa-table" aria-hidden="true"></i>
              </button> -->

            </div>
          </editor-menu-bar>

          <editor-content class="editor-box" :editor="editor"/>

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

          <br>
          <label for="persona-select">Choose Personas: </label>
          <br>
          <multiselect
                      @input="onInputChanged('personas')"
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
          <label>Choose Products</label>
          <multiselect
                      @input="onInputChanged('products')"
                      v-model="form.products" :options="product_options"
                      :multiple="true" :close-on-select="false"
                      :clear-on-select="false" :preserve-search="true"
                      placeholder="Pick some" label="name"
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
        </div>
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
          <b-button variant="info"
            href="javascript:void(0)" v-on:click='submitFiles()'>Upload</b-button>
          <br>
          <div
          v-for="uploadedFile in uploadedFiles"
          v-bind:key="uploadedFile.id + uploadedFile.filename">
            {{uploadedFile.filename}}
            <b-button
                  variant="outline-primary"
                  type="button"
                  :href ="'/api/insight/files/' + form.id + '?file_id=' + uploadedFile.id"
                  download>
              <i class="fa fa-file"></i>
            </b-button>
            <b-button variant="outline-primary" v-on:click="deleteFile(uploadedFile.id)"
                type="button" href="javascript:void(0)">&times;
            </b-button>
          </div>
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
          <b-button type="button" variant="primary" v-on:click='onAdd'>Add New Insight</b-button>
        </div>
      </div>
  </b-form>


  <hr>

  <playlist-add
              :style="{right:30+'px' , position: 'absolute'}"
              :key="form.id + 'playlist'"
              class="right"
              :source='"insight"'
              :source_id="form.id"/>

  <h4>Comments</h4>
  <comment-view v-if='form.id != null'
                :key="form.id + 'Comments'"
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
import { Editor, EditorContent, EditorMenuBar } from 'tiptap'
import {
  Blockquote,
  BulletList,
  CodeBlock,
  HardBreak,
  Heading,
  HorizontalRule,
  ListItem,
  OrderedList,
  TodoItem,
  TodoList,
  Bold,
  Code,
  Italic,
  Link,
  Strike,
  Underline,
  History,
  Table,
  TableHeader,
  TableCell,
  TableRow,
  TrailingNode,
  Placeholder,
} from 'tiptap-extensions'

export default {
  name: "insight-details",
  components : {
    'comment-view': CommentView,
    'editor-content': EditorContent,
    'editor-menu-bar': EditorMenuBar
  },
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
        personas: [],
        archived: false,
      },
      editor: null,
      file : null,
      uploadedFiles: [],
      editing: true,
      source: 'insights',
      experience_options: ["Positive", "Neutral", "Negative"],
      emotion_options: ["Pain", "Joyful", "Triumphiant", "Angry", "Calm", "Frustrated", "Surprised" , "Excited", "Confused"],
      journey_options: ["Aware", "Try", "Use", "Leave"],
      edited_fields: [],
      }
    },
    watch: {
      'editing': function () {
        this.editor.setOptions({editable: this.editing});
      },
    },
    computed: {
      persona_options(){
        return store.state.personas
      },

      product_options(){
        return store.state.products
      },
    },
    beforeMount() {
      const self = this;

      // UPDATE DATA ON CHANGES
      EventBus.$on('insight-selection-changed', async function(selection){

        if (selection === null) {
          self.editing = true;
          return
        }

        const {data} = await api.insightTableById(selection);

        self.form.id = data[0].id;
        self.form.title= data[0].title;
        self.form.description= data[0].description;
        self.form.content = data[0].content;
        self.editor.setContent(data[0].content);
        self.form.experience_vector= data[0].experience_vector;
        self.form.magnitude = data[0].magnitude;
        self.form.frequency= data[0].frequency;
        self.form.emotions = data[0].emotions;
        self.form.props = data[0].props;
        self.form.journey= data[0].journey;
        self.form.personas = data[0].personas;
        self.form.products = data[0].products;
        self.form.archived = data[0].archived;
        self.editing = false;
        self.edited_fields.length = 0 ;

        var response
        response = await api.insightFilesById(selection);
        self.uploadedFiles = response.data;
        });

        self.editor = new Editor({
            content: `<blockquote> highlights </blockquote>

                    <li>of users who may experience this: </li>
                    <li>segment :      </li>
                    <li>experience :    </li>
                    <li>journey :  </li>
                    <li>propositions :    </li>
                    <li>emotions : </li>

                    <h3>details</h3>

                    <blockquote> details</blockquote>


                    <blockquote> insights </blockquote>`,
            editable: self.editing,
            extensions: [
              new Blockquote(),
              new BulletList(),
              new CodeBlock(),
              new HardBreak(),
              new Heading({ levels: [1, 2, 3] }),
              new ListItem(),
              new OrderedList(),
              new TodoItem(),
              new TodoList(),
              new Link(),
              new Bold(),
              new Code(),
              new Italic(),
              new Strike(),
              new Underline(),
              new History(),
              new HorizontalRule(),
              new Table({
                resizable: true,
              }),
              new TableHeader(),
              new TableCell(),
              new TableRow(),
              new TrailingNode({
                node: 'paragraph',
                notAfter: ['paragraph'],
              }),
            ],
          })

    },
    mounted () {
      this.editor.on('update', ({getHTML }) => {
        this.form.content = getHTML()
        this.onInputChanged('content')
        })
    },

    beforeDestroy() {
      this.editor.destroy()
    },

    methods: {

      onInputChanged(field) {
          // add list of edited fields to array to reduce api calls on backend
          this.edited_fields.indexOf(field) === -1 ? this.edited_fields.push(field) : null
      },

      async onEdit() {
        var key;
        for (key of this.edited_fields) {
          const data = {[key] : this.form[key]}
          await api.insightTablePutById(this.form.id,data)
        };

        EventBus.$emit('insight-data-changed','item-updated');
        document.getElementById("right-sidepanel").style.width = "0px";
        this.$store.commit({
          type: 'alert',
          show : 2,           //seconds to auto dismiss
          variant : "success",
          content : "insight updated"
        })

      },

      async onAdd() {
        await api.insightPost(this.form)

        EventBus.$emit('insight-data-changed','item-updated');
        document.getElementById("right-sidepanel").style.width = "0px";
        this.$store.commit({
          type: 'alert',
          show : 2,           //seconds to auto dismiss
          variant : "success",
          content : "insight added"
          })
        },

      onReset() {
           // Reset our form values
           this.editing = false;
         },

      async onArchive() {
        const data = { 'archived': 1}
        await api.insightTablePutById(this.form.id,data)

        EventBus.$emit('insight-data-changed' , 'archived' )
        document.getElementById("right-sidepanel").style.width = "0px";
        this.$store.commit({
          type: 'alert',
          show : 3,           //seconds to auto dismiss
          variant : "warning",
          content : "insight archived, NOTE: data is not deleted, if this was done unintentially please reach out to the admin"
           })
        },

      submitFiles(){
          api.putInsightFilesById(this.form.id,this.file)
        },

      deleteFile(file_id){
          api.deleteInsightFilesById(this.form.id)
          // need to add action to update view
        },

      },


  };

</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>


<style scoped lang="scss">

b-form-input.h2 {
  font-family: inherit;
  border: none;
  background-color: transparent;
  color: inherit;
}

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

.expand_caret {
    transform: scale(1.6);
    transition: 0.2s;
    margin-left: 8px;
    margin-top: -4px;
}

div[aria-expanded='false'] > .expand_caret {
    transform: scale(1.6) rotate(-90deg);
}

.editor {
  position: relative;
  max-width: 30rem;
  margin: 0 auto 5rem auto;

  &__content {

    overflow-wrap: break-word;
    word-wrap: break-word;
    word-break: break-word;

    * {
      caret-color: currentColor;
    }

    pre {
      padding: 0.7rem 1rem;
      border-radius: 5px;
      background: black;
      color: white;
      font-size: 0.8rem;
      overflow-x: auto;

      code {
        display: block;
      }
    }

    p code {
      padding: 0.2rem 0.4rem;
      border-radius: 5px;
      font-size: 0.8rem;
      font-weight: bold;
      background: rgba(black, 0.1);
      color: rgba(black, 0.8);
    }

    ul,
    ol {
      padding-left: 1rem;
    }

    li > p,
    li > ol,
    li > ul {
      margin: 0;
    }

    a {
      color: inherit;
    }

    blockquote {
      border-left: 3px solid rgba(black, 0.1);
      color: rgba(black, 0.8);
      padding-left: 0.8rem;
      font-style: italic;

      p {
        margin: 0;
      }
    }

    img {
      max-width: 100%;
      border-radius: 3px;
    }

    table {
      border-collapse: collapse;
      table-layout: fixed;
      width: 100%;
      margin: 0;
      overflow: hidden;

      td, th {
        min-width: 1em;
        border: 2px solid grey;
        padding: 3px 5px;
        vertical-align: top;
        box-sizing: border-box;
        position: relative;
        > * {
          margin-bottom: 0;
        }
      }

      th {
        font-weight: bold;
        text-align: left;
      }

      .selectedCell:after {
        z-index: 2;
        position: absolute;
        content: "";
        left: 0; right: 0; top: 0; bottom: 0;
        background: rgba(200, 200, 255, 0.4);
        pointer-events: none;
      }

      .column-resize-handle {
        position: absolute;
        right: -2px; top: 0; bottom: 0;
        width: 4px;
        z-index: 20;
        background-color: #adf;
        pointer-events: none;
      }
    }

    .tableWrapper {
      margin: 1em 0;
      overflow-x: auto;
    }

    .resize-cursor {
      cursor: ew-resize;
      cursor: col-resize;
    }

  }
}

.menubar {

  margin-bottom: 1rem;
  transition: visibility 0.2s 0.4s, opacity 0.2s 0.4s;

  &.is-hidden {
    visibility: hidden;
    opacity: 0;
  }

  &.is-focused {
    visibility: visible;
    opacity: 1;
    transition: visibility 0.2s, opacity 0.2s;
  }

  &__button {
    font-weight: bold;
    display: inline-flex;
    background: transparent;
    border: 0;
    color: black;
    padding: 0.2rem 0.5rem;
    margin-right: 0.2rem;
    border-radius: 3px;
    cursor: pointer;

    &:hover {
      background-color: rgba(black, 0.05);
    }

    &.is-active {
      background-color: rgba(black, 0.1);
    }
  }

  span#{&}__button {
    font-size: 13.3333px;
  }
}

</style>
