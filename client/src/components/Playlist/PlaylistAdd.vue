
<template lang="html">
    <a v-if="isOnPlaylist === true" href="javascript:void(0)" @click="removeFromPlaylist()">
      <i class="fa fa-2x fa-bookmark active"></i>
    </a>
    <a v-else @click="addToPlaylist()">
      <i class="fa fa-2x fa-bookmark"></i>
    </a>
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

.fa {
  color: lightgrey;
}

.fa:hover {
  color: DarkGrey;
}

.fa.active {
  color: black;
}

</style>
