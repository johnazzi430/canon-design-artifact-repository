
<template lang="html">
  <div class="container main" :key="refresh_key">
    <h1>Playlist</h1>
    <div class="row">
      <div class="md-form mt-0 col-8" id="card-search">
        <input v-model="search"
          class="form-control"
          type="text"
          placeholder="Search for item"
          aria-label="Search">
      </div>
      <b-button-group class="mx-1">
<!-- <b-button variant="info" @click='toggleSearch(`"external":0`)'>
Clear Playlist</b-button> -->
        <b-button variant="info" @click='clearPlaylist()'>Clear Playlist</b-button>
      </b-button-group>
    </div>
    <br>
    <draggable v-model="cards" @start="drag=true" @end="drag=false">
        <b-card class="card" v-for="card in filterItems(cards)"
                v-bind:key="card.id + card.source"
                v-bind:class="[ card.experience_vector, card.source]">
          <b-card-text>
            <h4 style="text-align:left">{{card.source | capitalize}} id: {{card.id}}</h4>
            <div v-if="card.source ==='persona'">
              <div v-if="card.avatar == true">
                <img
                  v-bind:src="'/api/persona/avatar/' + card.id" class="avatar">
              </div>
              <div v-else>
                  <img src="../../../public/assets/img_avatar2.png"
                    alt="Avatar" class="avatar">
              </div>
            </div>
            {{card.name}}
            {{card.title}}
            {{card.description}}
            {{card.quote}}
            <div class="row">
              <b-button variant="outline-secondary" :to='"/"+card.source+"/" +card.id'>
                open <i class="fa fa-angle-double-right"></i>
              </b-button>
              <playlist-add
                    id="tooltip-target-1"
                    :style="{right:30+'px' , position: 'absolute'}"
                    :key="card.id"
                    :source='card.source'
                    :source_id="card.id"/>
            </div>
          </b-card-text>
          <!-- <b-button variant="outline-secondary"
                    v-on:click="removeFromPlaylist( card.source , card.id )">
            remove from playlist</b-button> -->
        </b-card>
    </draggable>

  </div>
</template>

<script type="text/javascript">
/*eslint-disable */
import api from '../../api'
import {EventBus} from "../../index.js";
import draggable from 'vuedraggable';
import PlaylistAdd from './PlaylistAdd.vue'


export default {
  name: 'playlist',
  components: {
    'playlist-add':PlaylistAdd,
    draggable
  },
  data() { return {
    cards : [
      {
      },
    ],
    isLoading: false,
    search : '',
    refresh_key: 0,
    options:{
      dropzoneSelector: 'ul',
      draggableSelector: 'li',
      handlerSelector: null,
      reactivityEnabled: true,
      multipleDropzonesItemsDraggingEnabled: true,
      showDropzoneAreas: true,
      onDrop: function(event) {},
      onDragstart: function(event) {},
      onDragenter: function(event) {},
      onDragend: function(event) {}
      }
    }
  },
  async mounted() {
    this.isLoading = true;
    const {data} = await api.getPlaylistDetails()
    this.isLoading = false;
    this.cards = data;
  },
  computed:{
  },
  methods:{
    removeFromPlaylist(source,id){
      const params = {
                    source_table : source,
                    source_id : id
                  }
      api.removeFromPlaylist(params)
      this.refresh_key += 1;
    },

    clearPlaylist: async function() {
      var card;
      for (card in this.cards) {
        const params= {
           source_table : this.cards[card].source,
           source_id : this.cards[card].id
         }
        api.removeFromPlaylist(params)
      }
      this.refresh_key += 1;
      this.cards = [];
    },

    toggleSearch(value) {
      if ( this.search != value){
        this.search = value
      }
      else {
        this.search = ''
      }
    },

    filterItems: function(cards) {
      var self = this;
      return cards.filter(function(cards) {
        let regex = new RegExp('(' + self.search+ ')', 'i');
//        return cards.name.match(regex);
        return JSON.stringify(cards).match(regex);
      })
    }
  },
};
</script>



<style lang="css" scoped>
.card-columns {
    column-count: 1;
}

.card.Negative{
  border-left-color: #FF5C42;
  border-left-style: solid;
  border-left-width: thick;
}

.card.Positive{
  border-left-color: green;
  border-left-style: solid;
  border-left-width: thick;
}

.card.Neutral{
  border-left-color: grey;
  border-left-style: solid;
  border-left-width: thick;
}

.card.product{
  border: 0px;
  border-top-style: solid;
  border-top-width: medium;
  border-image: linear-gradient(to right,#7799FF,purple) 1;
}

.avatar {
  width: 50px;
  height: 50px;
  display: block;
  object-fit: cover;
  margin-left: 0;
  margin-right: auto;
  border-radius: 50%;
}

.main{
  width: 100vh;
  height: 100vh;
  padding: 0px 10px;
  background-color: #F7F7F7
}


</style>
