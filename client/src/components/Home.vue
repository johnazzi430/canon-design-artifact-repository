<template lang="html">
  <div class="row h-100%">
    <div class="container my-auto" align="center">
      <button type="button" class="btn btn-outline-primary">
        <router-link to="/persona">
          <i class="fa fa-user fa-5x"></i>
          <h1>Persona</h1>
        </router-link></button>
      <button type="button" class="btn btn-outline-primary">
        <router-link to="/product">
          <i class="fa fa-laptop fa-5x"></i>
          <h1>Product</h1>
        </router-link></button>
      <button type="button" class="btn btn-outline-primary">
        <router-link to="/insights">
          <i class="fa fa-exclamation fa-5x"></i>
          <h1>Insights</h1>
        </router-link></button>
    </div>
    <div class="container" >
      <label>Files
        <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
      </label>
      <button href="javascript:void(0)" v-on:click="submitFiles()">Submit</button>
        <br>

      <div v-for="uploadedFile in uploadedFiles" v-bind:key="uploadedFile.id">
        {{uploadedFile.filename}}
        <button :href="'/api/personas/files/1?file_id='+uploadedFile.id"
          type="button" name="button" target="_blank">
          <i class="fa fa-file"></i>
          <button href="javascript:void(0)" v-on:click="getFile(uploadedFile.id)">
          Retrieve</button>
        </button>
      </div>
    </div>

  </div>
</template>


<script type="text/javascript">

/*eslint-disable */
import axios from 'axios'

export default {
    name: "file",
    data() {
      return {
        files: '' ,
        image: null,
        uploadedFiles: null}
    },

    beforeMount() {
      const self = this;
      axios({
      method: 'get',
      url: '/api/personas/files/1',
    }).then(function(response){
      self.uploadedFiles = response.data;
    })
  },

  methods: {

    getFile(file_id) {
        const self = this;
        axios({
        method: 'get',
        url: '/api/personas/files/1?file_id=' + file_id,
      }
      ).then(function(response){
        self.image = 'data:image/jpeg;base64,' + response.data[0]
        console.log(response);
      })
    },

    handleFileUpload(){
      this.file = this.$refs.file.files[0];
    },

    submitFiles(){

            let formData = new FormData();

            formData.append('file', this.file);
            formData.append('filename', 'blank');

            axios({
              method: 'post',
              url: '/api/personas/files/1',
              data : formData,
              headers: {
                    'Content-Type': 'multipart/form-data'
              }
            }
            ).then(function(response){
              console.log(response);
            })
            .catch(function(error){
              console.log(error);
            });
    },
  },
};


</script>

<style lang="css" scoped>
</style>
