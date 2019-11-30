<template>
  <div id="app">
    <app-nav></app-nav>
    <!-- <app-view>
      <app-sidebar></app-sidebar>
      <app-content></app-content>
    </app-view> -->
    <router-view/>
  </div>
</template>

<script>
/*eslint-disable */
import Nav from './components/Nav.vue';

export default {
  name: 'app',
  components: {
    'app-nav': Nav,
  },
  data() {
    return {
        authenticated: true,
        mockAccount: {
            username: "nraboy",
            password: "password"
        }
    }
  },
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
}


</style>
