

<template lang="html">
  <div class="container" :key="commentKey">
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
    <b-button v-b-toggle="'collapse-add-comment'" variant="success">Add Comment</b-button>
    <b-collapse :id="'collapse-add-comment'">
      <b-form-textarea v-model="form.comment"></b-form-textarea>
      <b-button v-on:click="addComment()" variant="success">Submit</b-button>
    </b-collapse>
  </div>
</template>

<script>
/*eslint-disable */
import axios from 'axios'
import {EventBus} from "../index.js";

export default {
  data() {
    return {
      commentKey: 0,
      comments : {},
      form :{
        comment:''
      }
    }
  },
  props: ["sourceTable" , "itemId"],
  beforeMount() {
      var get_url = "/api/"+ this.sourceTable+"/comments/" +this.itemId

      axios
      .get(get_url)
      .then(response => {this.comments = response.data})
      .catch(error => console.log(error))
    },
  methods:{
     async addComment() {

      var None = null
      var comment_data = {
        source_id : this.itemId,
        source_table : this.sourceTable,
        comment_body : this.form.comment,
        action : None,
        downchange : None,
        upchange : None,
      };

      var set_url = "/api/"+ this.sourceTable+"/comments/" +this.itemId

      axios({
          method: 'post',
          url: set_url,
          data: comment_data })
      .then(function (response) {
          console.log(response);
          EventBus.$emit('comments-added', comment_data );
          this.commentKey +1;
        })
      .catch(function (error) {
          console.log(error);})


    }
  }
};

</script>
