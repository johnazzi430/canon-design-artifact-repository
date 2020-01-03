

<template>
    <div>
      <b-navbar class="navbar-dark"
          style="padding-left:30px">
        <b-navbar-nav>
          <b-navbar-brand to="/">UTC Product Insight</b-navbar-brand>
          <b-nav-item to="/insights">Insights</b-nav-item>
          <b-nav-item to="/persona">Persona</b-nav-item>
          <b-nav-item to="/product">Product</b-nav-item>
          <b-nav-item disabled>Playlist</b-nav-item>
          <b-nav-item disabled>About</b-nav-item>
          <b-nav-item v-if="isLoggedIn" @click='logout'>Logout</b-nav-item>
          <b-nav-item v-if="userRole === 'admin'" to="/admin">Admin</b-nav-item>
        </b-navbar-nav>
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
  computed:{
    isLoggedIn : function() {return this.$store.getters.isLoggedIn},
    userRole : function() {return this.$store.getters.userRole}

  },
  methods: {
    async logout() {
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
  border-radius: 0;
}


</style>
