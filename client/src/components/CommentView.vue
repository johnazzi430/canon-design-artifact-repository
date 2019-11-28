

<template lang="html">
  <div class="container">
    {{sourceTable}} {{itemId}}
    <div class="col-5" v-for="comment in comments" v-bind:key="comment.id">
      <div class="" v-if="comment.action === null">
        <span> {{comment.creator_id}} commented on {{comment.create_date}}
        </span>
        <br>
        <p class="well">
          {{comment.comment_body}}
        </p>
      </div>
      <div class="" v-else>
        <i class="fa fa-edit"></i>
        <span> {{comment.creator_id}} {{comment.action}} {{comment.create_date}}
        </span>
      </div>
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
  props: ["sourceTable" , "itemId"],
  mounted(){
      var get_url = "http://localhost:5000/api/comments/" + this.sourceTable + '/' + this.itemId

      axios
      .get(get_url)
      .then(response => {this.comments = response.data})
      .catch(error => console.log(error))
    },
  // mounted () {
  //
  //   var get_url = "http://localhost:5000/api/comments/" + this.source_table + '/' + this.item_id
  //
  //   console.log(get_url)
  //   axios
  //   .get(get_url)
  //   .then(response => {this.comments = response.data})
  //   .catch(error => console.log(error))
  // },
};

</script>
