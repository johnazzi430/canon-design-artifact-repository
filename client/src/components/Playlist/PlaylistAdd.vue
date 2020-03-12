
<template lang="html">
  <div class="playlist-button">
    <a v-if="isOnPlaylist === true" href="javascript:void(0)" @click="removeFromPlaylist()">
      <span>
        <i id="bookmarked" class="fa-2x fas fa-bookmark active"></i>
        <span class="playlist-tooltip">Remove From Playlist</span>
      </span>
    </a>
    <a v-else @click="addToPlaylist()" href="javascript:void(0)">
      <span>
        <i id="not-bookmarked" class="fa-2x far fa-bookmark"></i>
        <span class="playlist-tooltip">Add to Playlist</span>
      </span>
    </a>

  </div>
</template>

<script>
/*eslint-disable */
import axios from 'axios'
import {EventBus} from "../../index.js";

export default {
  name: 'playlist-add',
  data() { return {
      isOnPlaylist: false,
    }
  },
  props : ["source","source_id"],
  methods:{
    addToPlaylist(){
      var self = this;
      axios({
           method: 'post',
           url: '/api/playlist',
           params: {
              source_table : self.source,
              source_id : self.source_id
            }
           })
      this.isOnPlaylist = true;

      self.$store.commit({
        type: 'alert',
        show : 2,           //seconds to auto dismiss
        variant : "info",
        content : self.source + " added to playlist"
      })

      console.log('added to playlist')
    },
    removeFromPlaylist(){
      var self = this;
      axios({
           method: 'Delete',
           url: '/api/playlist',
           params: {
              source_table : self.source,
              source_id : self.source_id
            }
           })
      this.isOnPlaylist = false;

      self.$store.commit({
        type: 'alert',
        show : 2,           //seconds to auto dismiss
        variant : "info",
        content : self.source + " removed from playlist"
      })

      console.log('removed from playlist')
    }
  },
  beforeMount() {

      const self = this;
      var get_url = `/api/playlist`;
      var resp

      axios.get(get_url)      // CHECKS TO SEE IF ON USERS PLAYLIST
      .then(response => {
        self.resp = response.data
        self.resp.forEach((item) => {
          if( item.source_table == self.source && item.source_id == self.source_id) {
            self.isOnPlaylist = true;
          }
        })
      })
      .catch(error => console.log(error))
  },
};
</script>

<style lang="css" scoped>

.playlist-button .playlist-tooltip {
  top: -5px;
  right: 105%;
  visibility: hidden;
  width: 120px;
  background-color: black;
  color: #fff;
  text-align: center;
  padding: 5px 0;

  /* Position the tooltip */
  position: absolute;
  z-index: 1;
}

.playlist-button:hover .playlist-tooltip {
  visibility: visible;
}

.fa-bookmark {
  color: lightgrey;
}

.fa-bookmark:hover {
  color: DarkGrey;
}

.fa-bookmark.active {
  color: black;
}

</style>
