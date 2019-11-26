

<template lang="html">
  <div class="container">
    <div class="col-5" v-for="comment in comments" v-bind:key="comment.id">
      <span> {{comment.creator_id}} commented on {{comment.create_date}}
      </span>
      <br>
      <p class="well">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Quisque at augue at leo hendrerit commodo.
        Pellentesque auctor non quam eget lobortis.
      </p>
    </div>
    <div class="row" id="comment-action">
      <mdb-icon icon="edit" />
    </div>

    <b-button href="javascript:void(0)" variant="success">Add Comment</b-button>
  </div>
</template>

<script>
/*eslint-disable */
import axios from 'axios'
import {EventBus} from "../event-bus.js";

export default {
  data() {return { comments : {} } },
  beforeMount() {
    const self = this;
    var get_url = "http://localhost:5000/api/comments/PERSONA/40";

    axios.get(get_url)
    .then(response => {
      self.comments = response.data
    }
    )
    .catch(error => console.log(error))
  },
};

</script>
