

<template>
    <div>
      <b-navbar class="navbar navbar-expand-md navbar-light "
          style="padding-left:30px">
        <div class="navbar-nav">
          <b-navbar-brand to="/">UTC Product Insight</b-navbar-brand>
          <!-- <b-nav-item :to="{path :'/'}">Home</b-nav-item>
          <b-nav-item :to="{path :'/persona'}">Personas</b-nav-item >
          <b-nav-item :to="{path :'/product'}">Products</b-nav-item>
          <b-nav-item :to="{path :'/login'}">login</b-nav-item> -->
          <b-nav-item to="/insights">Insights</b-nav-item>
          <b-nav-item to="/persona">Persona</b-nav-item>
          <b-nav-item to="/product">Product</b-nav-item>
          <!-- <b-nav-item disabled to="/insights">Insights</b-nav-item> -->
          <b-nav-item>Playlist</b-nav-item>
          <b-nav-item to="/login">About</b-nav-item>
          <b-nav-item v-if="isLoggedIn" @click='logout'>Logout</b-nav-item>
          <b-nav-item v-if="userRole === 'admin'" to="/admin">Admin</b-nav-item>
        </div>
      </b-navbar>
    </div>
</template>

<script>
/*eslint-disable */
import store from  "../store";

export default {
  data() {
    return {
      role : null
    }
  },
  computed :{
    isLoggedIn : function() {return this.$store.getters.isLoggedIn},
    userRole : function() {return this.$store.getters.userRole}
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
      this.$router.push('/login')
    },
  },
  mounted() {
    this.role = this.$store.state.role
  }
}

</script>


<style >
.navbar {
  z-index: 100;
  margin-bottom: -15px;
  background-color: #F0F0F0
}
</style>
