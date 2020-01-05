
<template lang="html">
  <div class="container main">
    <h1>Playlist</h1>
    <div class="md-form mt-0" id="card-search">
      <input v-model="search"
        class="form-control"
        type="text"
        placeholder="Search for item"
        aria-label="Search">
    </div>
    <b-card-group columns v-drag-and-drop:options="options">
      <b-card class="card" v-for="card in filterItems(cards)"
              v-bind:key="c ard.id + card.source"
              v-bind:class="[ card.experience_vector, card.source]">
        <b-card-text>
          <h4 style="text-align:left">{{card.source | capitalize}} id: {{card.id}}</h4>
          <div v-if="card.source ==='persona'">
            <img src="../../public/assets/img_avatar2.png" alt="Avatar" class="avatar" align="left">
          </div>
          {{card.name}}
          {{card.title}}
          {{card.description}}
          {{card.quote}}
          <b-button variant="outline-secondary" :to='"/"+card.source+"/" +card.id'>
            open <i class="fa fa-angle-double-right"></i>
          </b-button>
        </b-card-text>
        <!-- <b-button variant="outline-secondary"
                  v-on:click="removeFromPlaylist( card.source , card.id )">
          remove from playlist</b-button> -->
      </b-card>
    </b-card-group>
  </div>
</template>

<script type="text/javascript">
/*eslint-disable */
import axios from 'axios'
import {EventBus} from "../index.js";
import PlaylistAdd from './Playlist/PlaylistAdd.vue'


export default {
  name: 'playlist',
  components: {
    'playlist-add':PlaylistAdd,
  },
  data() { return {
    cards : [],
    search : '',
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
  beforeCreate() {
    const self = this;
    var user_id = 1
    var get_url = `/api/playlist/` + user_id +'?details=True';

    axios.get(get_url)
    .then(response => {
      self.cards = response.data
    })
    .catch(error => console.log(error))
  },
  computed:{
  },
  methods:{
    removeFromPlaylist: async function(source,id) {
      await axios({
           method: 'delete',
           url: '/api/playlist',
           params: {
              user_id : 1,
              source_table : source,
              source_id : id
            }
           })
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
  min-width: 50px;
  max-width: 50px;
  min-height: 50px;
  max-height: 50px;
  display: block;
  margin-left: auto;
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
