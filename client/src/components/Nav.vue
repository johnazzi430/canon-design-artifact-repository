

<template>
    <div>
      <b-navbar
          toggleable="sm"
          class="navbar-expand-lg navbar-dark"
          style="padding-left:30px; border-radius: 0px">
        <b-navbar-nav>
          <b-navbar-brand to="/">
                        UTC Canon
                        <h6 class='subscript'>Product Artifact Repository</h6>
          </b-navbar-brand>
          <b-nav-item to="/insight">Insight</b-nav-item>
          <b-nav-item to="/persona">Persona</b-nav-item>
          <b-nav-item to="/product">Product</b-nav-item>
          <b-nav-item to="/playlist">Playlist</b-nav-item>
          <b-nav-item to="/about">About</b-nav-item>
          <b-nav-item v-if="user.role == 'admin'" to="/admin">Admin</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav v-if="isLoggedIn" class="ml-auto">
          <b-nav-item>
          <rotor-avatar accent="accent-1" icon="rotor-icon-user"
                        initials="A" is-clickable="false" /> </b-nav-item>
          <b-nav-item>User: {{user.username.split("@")[0] }} </b-nav-item>
          <b-nav-item @click='logout'>Logout</b-nav-item>
        </b-navbar-nav>
      </b-navbar>
    </div>
</template>

<script>
/*eslint-disable */
import {store} from  "../store";
import axios from 'axios'

export default {
  computed:{
    isLoggedIn : function() {return this.$store.getters.isLoggedIn},
    user : function() {return this.$store.getters.user},
  },
  methods: {
    async logout() {

      await axios({
        method : 'post',
        url : `/api/logout`
      })

      this.$store.dispatch('logout')
      this.$router.push('/login')
    },
  },
}

</script>


<style>
.navbar {
  z-index: 100;
  margin-bottom: -15px;
  background-color: #000000;
  color: #FFFFFF;
}

.subscript {
  margin:0;
}

</style>
