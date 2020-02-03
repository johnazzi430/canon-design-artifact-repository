<template>
  <div id="app">
    <app-nav></app-nav>
    <!-- <div class="container">
      <button v-on:click='SendAlert()'> CLICK ME!</button>
    </div> -->
    <!-- <div class="wrapper" v-if="alert.show">
      <b-alert
              class="alert"
              v-model="this.$store.state.alert"
              :variant="this.$store.state.alert.variant"
              @dismissed="this.$store.state.alert.show=false"
              dismissible>
        {{this.$store.state.alert.content}}
      </b-alert>
    </div> -->
    <router-view/>
  </div>
</template>

<script>
/*eslint-disable */
import Nav from './components/Nav.vue';
import axios from 'axios';
import {store} from  "./store";

export default {
  name: 'app',
  components: {
    'app-nav': Nav,
  },
  data () {
    return {
      image: ''
    }
  },
  beforeCreate() {
      this.$store.dispatch('enter')
  },
  created: function () {
    this.$http.interceptors.response.use(undefined, function (err) {
      return new Promise(function (resolve, reject) {
        if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
          this.$store.dispatch(logout)
        }
        throw err;
      });
    });
  },
  computed :{
    alert() {
      this.$store.state.alert
    }
  },
  methods :{

    getImage(){
        this.image = '/api/persona/avatar/53'
    },

    SendAlert() {
        this.$store.commit({
          type: 'alert',
          alert : {
            show : true,
            variant : "info",
            content : "TESTING!"
          },
        })
    }
  },
}


</script>

<style>

body, html {
  padding: 0;
  margin: 0;
  width: 100%;
  min-height: 100%;
  background-color: #F7F7F7;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
  background: #F7F7F7;
}

.alert{
  position: fixed;
  z-index: 1000;
  left: 0px;
  top: 0px;
}

</style>
