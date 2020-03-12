<template lang="html">
     <!-- eslint-disable max-len -->
  <div class="wrapper">
    <div class="container">

      <h1>Can·on</h1>
      <p><i>noun.</i> the body of rules, principles, or standards accepted as axiomatic and universally binding in a field of study or art</p>

      <br>
      <h1>About</h1>
      <hr>
      <p>Large firms often have trouble managing products in a cohesive manner across porduct teams, it requires
        overhead, management and coordination that often is lost especially in less tech forward firms. This product
        is designed to provide a singular place for product teams to store share and collaborate design artifacts such as customer insight
        in a light-weight way.
      </p>
      <hr>
      <h2>Components:</h2>
      <h3>Insights</h3>
      <p>Singular “nuggets” of user information, representing the base level of
        knowledge of a particular user at a particular time, and their feedback
        on an interaction with on of our digital products
      </p>

      <h3>Personas</h3>
      <p>Collection of information that describes a certain user group that will
        or might be using a digital product
      </p>

      <h3>Products</h3>
      <p>Individual digital assets that represent a consistent experience and
        provide value to users through a digital journey
      </p>
      <hr>
      <h3>Versioning</h3>
      <p>v0.0.8 - Beta Release</p>
      <hr>
      <h3>Contributing and Feedback</h3>
      <a href="https://github.com/johnazzi430/canon-design-artifact-repository">github.com/canon-design-artifact-repository</a>
      <hr>
    </div>

  </div>
</template>

<script type="text/javascript">
/*eslint-disable */


export default {
  data() {

  },
  methods: {
    changeView(view) { this.selection = view},
  }
}

</script>

<style media="screen" scoped>
.sidepanel-left{
  z-index:1;
  position:fixed;
  left:0;
  top:0;
  padding-top: 70px;
  width: 200px;
  height: 100VH;
  background-color: #F7F7F7;
  border-right-style: solid;
  border-right-color: #D1D1D1;
  border-right-width: thin;
  white-space: nowrap;
}

.nav-text{
  width:60px;
  padding-left:10px;
}

.nav-link{
  padding:15px;
  font-size: 15px;
}

#main {
  margin-left: 200px;
  width: 100vl;
  padding: 0px 10px;
  white-space:normal;
}

.wrapper {
    display: flex;
    width: 100vl;
    align-items: stretch;
    margin-top:-16px;
    padding-top:-16px;
}
</style>
