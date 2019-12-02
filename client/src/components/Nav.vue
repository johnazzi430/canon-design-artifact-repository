

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
          <router-link to="/">Home</router-link> |
          <router-link to="/persona">API Sample</router-link>
          <router-link to="/product">API Sample</router-link>
          <router-link to="/login">API Sample</router-link>
        </div>
      </b-navbar>
    </div>
</template>

<style>
.navbar {
  z-index: 100;
  margin-bottom: 0px;
}
</style>
