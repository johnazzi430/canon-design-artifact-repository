<template>
  <div id="app">
    <app-nav></app-nav>
    <!-- <div class="container">
      <button v-on:click='SendAlert()'> CLICK ME!</button>
    </div> -->

    <div v-for="(alert, index) in this.$store.state.alert.slice().reverse()"
      v-bind:key="alert.time"
      class="alert-container"
      v-bind:style="{top:60+index*50 +'px'}">
        <b-alert
                fade
                class="alert"
                :variant="alert.variant"
                :show="alert.show"
                @dismissed="alert.show=false"
                dismissible>
                {{alert.content}}
        </b-alert>
    </div>

    <router-view/>

    <!-- <a href="javascript:void(0)"
       :style="{right:30+'px', bottom:30+'px'}"
       @click='logout'>Logout</a> -->
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
    async logout() {

      await axios({
          method : 'post',
          url : `/api/logout`
        })

      this.$store.dispatch('logout')
      this.$router.push('/login')
    },

    SendAlert() {
        this.$store.commit({
          type: 'alert',
          show : 5,           //seconds to auto dismiss
          variant : "info",
          content : "TESTING!"
        })
    }
  },
}


</script>

<style>

.body, html {
  padding: 0;
  margin: 0;
  width: 100%;
  height: 100%;
  min-height: 100%;
  background-color: #F7F7F7;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
  height: 100%;
  background: #F7F7F7;
}

.alert{
  z-index: 10000;
  width: 100%
}

.alert-container{
  z-index: 10000;
  position: fixed;
  width: 100%;
}

</style>
