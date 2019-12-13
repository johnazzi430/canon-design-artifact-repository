

<template>
    <div>
      <b-navbar class="navbar navbar-expand-md navbar-light bg-light"
          style="padding-left:30px">
        <div class="navbar-nav">
          <b-navbar-brand>UTC User Personas</b-navbar-brand>
          <!-- <b-nav-item :to="{path :'/'}">Home</b-nav-item>
          <b-nav-item :to="{path :'/persona'}">Personas</b-nav-item >
          <b-nav-item :to="{path :'/product'}">Products</b-nav-item>
          <b-nav-item :to="{path :'/login'}">login</b-nav-item> -->
          <b-nav-item to="/">Home</b-nav-item>
          <b-nav-item to="/persona">Persona</b-nav-item>
          <b-nav-item to="/product">Product</b-nav-item>
          <b-nav-item to="/insights">Insights</b-nav-item>
          <!-- <b-nav-item disabled to="/insights">Insights</b-nav-item> -->
          <b-nav-item to="/login">Login</b-nav-item>
          <b-nav-item v-if="role === 'Admin'" to="/admin"></b-nav-item>
        </div>
      </b-navbar>
    </div>
</template>

<script>
/*eslint-disable */
import store from  "../store";

export default {
  beforeMount() {
    this.role = this.$store.state.role
  }
}

</script>


<style >
.navbar {
  z-index: 100;
  margin-bottom: 0px;
}
</style>
