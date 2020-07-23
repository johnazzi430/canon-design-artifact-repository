
<template lang="html">
  <div class="container" :key="commentKey">
    <div class="wrapper" v-if="comments !== null">
      <div v-for="(comment, index) in comments" v-bind:key="index">
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
      <b-form-textarea autofocus v-model="form.comment"></b-form-textarea>
      <b-button
        v-on:click="addComment()" variant="success">Submit</b-button>
    </b-collapse>
    <br>
  </div>
</template>

<script>
/*eslint-disable */
import axios from 'axios'
import api from '../api'
import {EventBus} from "../index.js";
import store from '../store'

export default {
  data() {
    return {
      commentKey: 0,
      comments : [],
      addingcomment: false,
      form :{
        comment:''
      }
    }
  },
  props: ["sourceTable" , "itemId"],
  async mounted() {
    const {data} = await api.getItemComments(this.sourceTable,this.itemId)
    this.comments = data

    // let self = this
    // EventBus.$on('comments-added', async function(){
    //   const {data} =  await api.getItemComments(self.sourceTable,self.itemId)
    //   self.comments = data
    // });
  },
  methods:{

    formatDate(value) {
      if (value) {
        return moment(String(value)).format('MM/DD/YYYY')
      }
    },

     async addComment() {
       this.addingcomment=true

        var None = null
        var comment_data = {
          source_id : this.itemId,
          source_table : this.sourceTable,
          comment_body : this.form.comment,
          action : None,
          downchange : None,
          upchange : None,
        };

        await api.addComment(this.sourceTable,this.itemId,comment_data)

        EventBus.$emit('comments-added', comment_data );
        comment_data.user = store.state.user
        this.comments.push(comment_data)
        this.addingcomment = false
        this.commentKey = +1
    },
  }
};


</script>
