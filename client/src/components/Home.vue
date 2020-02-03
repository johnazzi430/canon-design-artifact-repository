<template lang="html">
  <div class="">
    <div class="container purple-gradient" align="center">
      <button type="button" class="btn btn-outline-primary">
        <router-link to="/insight">
          <i class="fa fa-exclamation fa-5x"></i>
          <h1>Insight</h1>
        </router-link></button>
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
    </div>
    <hr>
  </div>
</template>


<style lang="css" scoped>

.btn {
  flex: 1 1 auto;
  margin: 10px;
  padding: 30px;
  text-align: center;
  text-transform: uppercase;
  transition: 0.5s;
  background-size: 200% auto;
  color: white;
 /* text-shadow: 0px 0px 10px rgba(0,0,0,0.2);*/

 box-shadow:
   -8px -8px 8px 0 rgba(255,255,255,0.5),
   8px 8px 8px 0 rgba(0,0,0,0.1);
  border-radius: 10px;
 }

.btn:hover {
  background-position: right center; /* change the direction of the change here */
  background-color: white;
}

/* .btn {
  background-image: linear-gradient(to right, #fbc2eb 0%, #a6c1ee 51%, #fbc2eb 100%);
} */


</style>
