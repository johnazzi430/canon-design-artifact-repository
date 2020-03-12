<template>
    <div>
      <b-alert :show='this.$store.state.authenticated===false' variant="info" dismissible>
          Please log in..
      </b-alert>
      <div id="login" v-if='form_mode === "login"'>
        <h1>Login</h1>
          <input required type="text" name="username"
            v-model="input.username" placeholder="Email" /><br><br>
          <input required id='password' type="password" name="password"
            v-model="input.password" placeholder="Password" /><br><br>
          <div class="row">
            <button type="button" class="btn btn-outline-secondary"
              v-on:click="login()">login</button>
            <button type="button" class="btn btn-outline-secondary"
              v-on:click="changeView('register')">register</button>
            <button type="button" class="btn btn-outline-secondary"
              v-on:click="changeView('reset_password')">reset password</button>
          </div>
          <a href="mailto:blank">Request help</a>
      </div>
      <div id="login" v-else-if='form_mode === "register"'>
        <h1>Register</h1>
        <input type="text" name="username" v-model="input.username" placeholder="Email" /><br><br>
        <input id='password' type="password" name="password"
          v-model="input.password" placeholder="Password" /><br><br>
        <div class="row">
          <button type="button" class="btn btn-outline-secondary"
            v-on:click="changeView('login')">cancel</button>
          <button type="button" class="btn btn-outline-secondary"
            v-on:click="register()">register</button>
        </div>
        <a href="mailto:blank">Request help</a>
      </div>
      <div id="login" v-else-if='form_mode === "reset_password"'>
        <h1>Change Password</h1>
          <input type="text" name="username" v-model="input.username" placeholder="Email" /><br><br>
          <input id='password' type="password" name="password"
              v-model="input.password" placeholder="Current Password" /><br><br>
          <input type="password" name="password"
              v-model="input.new_password" placeholder="New Password" /><br><br>
          <div class="row">
            <button type="button" class="btn btn-outline-secondary"
            v-on:click="changeView('login')">back</button>
            <button type="button" class="btn btn-outline-secondary"
            v-on:click="changeView('reset_password')">Change Password</button>
            <button type="button" class="btn btn-outline-secondary"
            v-on:click="changeView('reset_password')">forgot password?</button>
          </div>
          <a href="mailto:blank">Request help</a>
      </div>


    </div>
</template>

<script>
/*eslint-disable */
import store from  "../../store";
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      input: {
        username: "",
        password: "",
        new_password:""
      },
      form_mode: "login",
    }
  },
  beforeMount() {
  },

  methods: {

    changeView(view) {
      this.form_mode = view
    },


    login: function() {
      const self = this;

      let username = this.input.username
      let password = this.input.password

      this.$store.dispatch('login',{username,password})
      .then(function (response) {

           self.$store.commit({
             type: 'alert',
             show : 2,           //seconds to auto dismiss
             variant : "info",
             content : "User Logged In"
           })

           self.$router.push("/")
      })
      .catch(function (error) {
          self.$store.commit({
            type: 'alert',
            show : true,           //seconds to auto dismiss
            variant : "danger",
            content : "The username and / or password is incorrect"
          })
          console.log("The username and / or password is incorrect");
           })

    },

    register() {
      const self = this

      if(this.input.username != "" && this.input.password != "" && this.input.username.includes(".com")) {
        axios({
            method: 'post',
            url: '/api/users',
            data: self.input,
            header: {
              "Content-Type":"application/json"
            }
          })
        .then(function (response) {
            console.log(response);
            self.input.authenticated = response.data[0].authenticated
          })
        .catch(function (error) {
            console.log(error);
          })

          self.$store.commit({
            type: 'alert',
            show : 10,           //seconds to auto dismiss
            variant : "info",
            content : "Succesfully Registered Please log in when you get approval"
          })

          }
        else {
          self.$store.commit({
            type: 'alert',
            show : 2,           //seconds to auto dismiss
            variant : "danger",
            content : "An email is required"
          })
        }
    },
    reset_password(){
    },
  },
}
</script>

<style scoped>

  .row {
    align-content: center;
    text-align: center;
    margin: 0px 0px;
  }

    #login {
        margin: 20px;
        padding: 20px;
        position: relative;
        left: 0px;
        top: 100px;
        width: 400px;
        height: 400px;
        border: 1px solid #CCCCCC;
        background-color: #FFFFFF;
    }
</style>
