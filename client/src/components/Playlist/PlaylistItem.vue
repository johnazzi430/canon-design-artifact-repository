<template lang="html">
  <div class="container">
    <b-card>
      <h1>Playlist</h1>
      {{card}}
    </b-card>
  </div>
</template>

<script type="text/javascript">
/*eslint-disable */
import axios from 'axios'
import {EventBus} from "../index.js";

export default {
  data() { return {
    card : [],
    search : ''
    }
  },
  props =["source","source_id"]
  beforeCreate()
      const self = this;

      switch (self.source) {
        case "persona":
          var get_url = `/api/persona-table/` + self.source_id;
          break;
        case "product":
          var get_url = `/api/product-table/` + self.source_id;
          break;
        case "insight":
          var get_url = `/api/insights/` + self.source_id;
          break;
        }

        axios.get(get_url)
              .then(response => {
                    self.card = response.data
                  })
  },
  methods:{
  },
};
</script>

<style lang="css" scoped>

</style>
