<template>
    <div>
        <b-alert :show='this.$store.state.authenticated===false' variant="info" dismissible>
          Please log in..
      </b-alert>
        <b-alert v-model="alert.show" :variant="alert.variant" dismissible>
        {{alert.text}}
      </b-alert>
      <div id="login" v-if='form_mode === "login"'>
        <h1>Login</h1>
          <input required type="text" name="username"
            v-model="input.username" placeholder="Email" />
          <input required id='password' type="password" name="password"
            v-model="input.password" placeholder="Password" />
          <div class="row">
            <button type="button" class="btn btn-outline-secondary"
              v-on:click="login()">login</button>
            <button type="button" class="btn btn-outline-secondary"
              v-on:click="changeView('register')">register</button>
            <button type="button" class="btn btn-outline-secondary"
              v-on:click="changeView('reset_password')">reset password</button>
          </div>
      </div>
      <div id="login" v-else-if='form_mode === "register"'>
        <h1>Register</h1>
        <input type="text" name="username" v-model="input.username" placeholder="Email" />
        <input id='password' type="password" name="password"
          v-model="input.password" placeholder="Password" />
        <div class="row">
          <button type="button" class="btn btn-outline-secondary"
            v-on:click="changeView('login')">cancel</button>
          <button type="button" class="btn btn-outline-secondary"
            v-on:click="register()">register</button>
        </div>
      </div>
      <div id="login" v-else-if='form_mode === "reset_password"'>
        <h1>Change Password</h1>
          <input type="text" name="username" v-model="input.username" placeholder="Email" /><br>
          <input id='password' type="password" name="password"
              v-model="input.password" placeholder="Current Password" /><br>
          <input type="password" name="password"
              v-model="input.new_password" placeholder="New Password" /><br>
          <div class="row">
            <button type="button" class="btn btn-outline-secondary"
            v-on:click="changeView('login')">back</button>
            <button type="button" class="btn btn-outline-secondary"
            v-on:click="changeView('reset_password')">Change Password</button>
            <button type="button" class="btn btn-outline-secondary"
            v-on:click="changeView('reset_password')">forgot password?</button>
          </div>
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
      alert : {
        show : false,
        text : "",
        variant : "danger",
      },
      form_mode: "login",
    }
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
           self.alert.show = true;
           self.alert.text = "logged in...";
           self.alert.variant = 'success';
           self.$router.push("/")
      })
      .catch(function (error) {
          console.log(error);
          self.alert.show = true;
          self.alert.text = "The username and / or password is incorrect";
          self.alert.variant = 'danger';
          console.log("The username and / or password is incorrect");
           })

      // if(self.input.username != "" && self.input.password != "") {
      //   axios({
      //       method: 'post',
      //       url: '/api/login',
      //       data: self.input,
      //       header: {
      //         "Content-Type":"application/json"
      //       }
      //     })
      //   .then(function (response) {
      //       console.log(response);
      //       self.input.authenticated = response.data
      //       if ( self.input.authenticated === true) {
      //         self.$emit("authenticated", true);
      //         store.state.authenticated = true;
      //         store.state.role= response.data.role;
      //         console.log("succesfull login")
      //         self.alert.show = true;
      //         self.alert.text = "logged in...";
      //         self.alert.variant = 'success';
      //         self.$router.push("/")
      //       }
      //       else {
      //         self.alert.show = true;
      //         self.alert.text = "The username and / or password is incorrect";
      //         self.alert.variant = 'danger';
      //         console.log("The username and / or password is incorrect");
      //       }
      //     })
      //   .catch(function (error) {
      //       console.log(error);})
      // }
      // else {
      //   self.alert.show = true;
      //   self.alert.text = "A username and password must be present";
      //   self.alert.variant = 'danger';
      //   console.log("A username and password must be present");
      // }
    },

    register() {
      const self = this

      if(this.input.username != "" && this.input.password != "" && this.input.username.includes("utc.com")) {
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

          this.form_mode = 'login'
          this.alert.show = true;
          this.alert.text = "Succesfully registered, please login...";
          this.alert.variant = 'success';

          }
        else {
          this.alert.show = true;
          this.alert.text = "A UTC email must be definied";
          this.alert.variant = 'danger';
        }
    },
    reset_password(){
    },
  },
}
</script>

<style scoped>
    #login {
        width: 500px;
        border: 1px solid #CCCCCC;
        background-color: #FFFFFF;
        margin: auto;
        margin-top: 200px;
        padding: 20px;
    }
</style>
