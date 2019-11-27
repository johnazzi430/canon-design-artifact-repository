

<template lang="html">
  <div class="container">
    {{source_table}}
    {{item_id}}
    <div class="col-5" v-for="comment in comments" v-bind:key="comment.id">
      <div class="" v-if="comment.action === null">
        <span> {{comment.creator_id}} commented on {{comment.create_date}}
        </span>
        <br>
        <p class="well">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          Quisque at augue at leo hendrerit commodo.
          Pellentesque auctor non quam eget lobortis.
        </p>
      </div>
      <div class="" v-else>
        <p class="well">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          Quisque at augue at leo hendrerit commodo.
          Pellentesque auctor non quam eget lobortis.
        </p>
      </div>
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
  props: ["source_table" , "item_id"],
  beforeMount() {
    var get_url = "http://localhost:5000/api/comments/";
    // get_url = "http://localhost:5000/api/comments/PERSONA/40";
    get_url =+ this.source_table + '/' + this.item_id;

    console.log(get_url)
    axios.get(get_url)
    .then(response => {this.comments = response.data})
    .catch(error => console.log(error))
  },
};

</script>
