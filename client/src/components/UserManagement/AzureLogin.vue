<template>
  <div>
    <b-button @click="login" type="button" v-if="!user" variant='info' block id="AD-Button">
      <div class="row">
        <i class="fab fa-microsoft fa-2x"></i>
        <h4>Login with Azure AD</h4>
      </div>
    </b-button>
    <b-button @click="logout" type="button" v-if="user">
      <i class="fab fa-microsoft"></i> Logout
    </b-button>
    <h3 v-if="user">Hello {{ user.name }}</h3>
    <pre v-if="userInfo">{{ JSON.stringify(userInfo, null, 4) }}</pre>
    <p v-if="loginFailed">Login unsuccessful</p>
    <p v-if="apiCallFailed">Graph API call unsuccessful</p>
  </div>
</template>

<script>
/*eslint-disable */

export default {
  data() {
    return {
      user: null,
      userInfo: null,
      apiCallFailed: false,
      loginFailed: false
    }
  },
  methods: {
    logout() {
      this.$AuthService.logout();
    },

    login() {
      this.$AuthService.login();
    },
  }
};

</script>

<style scoped>

  .row {
    align-content: center;
    text-align: center;
    margin: 0px 10px;
  }

  i {

        margin: 0px 10px;
  }
  h4 {
        margin: 0px 10px;
  }

</style>
