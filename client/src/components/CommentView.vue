
<template lang="html">
  <div class="container" :key="commentKey">
    <div class="wrapper" v-if="comments !== null">
      <div v-for="comment in comments" v-bind:key="comment.id">
        <div class="" v-if="comment.action === null">
          <span> {{comment.user.username}} commented {{comment.create_date | formatDate}}
          </span>
          <br>
          <p class="well">
            {{comment.comment_body}}
          </p>
        </div>
        <div class="" v-else>
          <i class="fa fa-edit"></i>
          <span>
            {{comment.user.username}} {{comment.action}}
            {{comment.create_date | formatDate}}
          </span>
        </div>
      </div>
    </div>
    <b-button
      v-if="this.$store.getters.isLoggedIn"
      v-b-toggle="'collapse-add-comment'"
      variant="success">Add Comment</b-button>
    <b-collapse :id="'collapse-add-comment'">
      <b-form-textarea v-model="form.comment"></b-form-textarea>
      <b-button
        v-on:click="addComment()" variant="success">Submit</b-button>
    </b-collapse>
    <br>
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
  mounted() {
    const self = this

    EventBus.$on('comments-added', function(){
      var get_url = "/api/"+ self.sourceTable+"/comments/" +self.itemId

      axios
      .get(get_url)
      .then(response => {self.comments = response.data})
      .catch(error => console.log(error))
    });
  },
  methods:{

    formatDate(value) {
      if (value) {
        return moment(String(value)).format('MM/DD/YYYY')
      }
    },

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

        const data = await axios({
            method: 'post',
            url: set_url,
            data: comment_data })

        EventBus.$emit('comments-added', comment_data );

    },

  }
};


</script>
