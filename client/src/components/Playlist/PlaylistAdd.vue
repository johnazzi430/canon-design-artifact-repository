
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

import api from '../../api'
import store from '../../store'
import {EventBus} from "../../index.js";

export default {
  name: 'playlist-add',
  data() { return {
      isOnPlaylist: false,
    }
  },
  props : ["source","source_id"],
  methods:{
    async addToPlaylist(){
      const params = {
                    source_table : this.source,
                    source_id : this.source_id,
                  }
      await api.addToPlaylist(params)
      this.isOnPlaylist = true;

      store.dispatch('getPlaylist')

      store.commit({
        type: 'alert',
        show : 2,           //seconds to auto dismiss
        variant : "info",
        content : this.source + " added to playlist"
      })

      console.log('added to playlist')
    },
    async removeFromPlaylist(){
      const params = {
                    source_table: this.source,
                    source_id: this.source_id,
                  }
      await api.removeFromPlaylist(params)
      this.isOnPlaylist = false;
      store.dispatch('getPlaylist')

      store.commit({
        type: 'alert',
        show : 2,           //seconds to auto dismiss
        variant : "info",
        content : this.source + " removed from playlist"
      })

      console.log('removed from playlist')
    }
  },
  beforeMount() {
      if(store.getters.isItemOnPlaylist(this.source,this.source_id)){
        this.isOnPlaylist = true;
      }
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
