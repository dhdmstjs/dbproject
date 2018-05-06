<template>
  <div id="app">
    <v-app>
      <div v-if="this.login==false">
      <!-- Login/Register -->
      <v-layout row wrap justify-end>
        <v-flex xs4>
        <v-btn color="primary" dark @click.stop="loginfunc = true">Login</v-btn>
        <v-btn color="primary" dark @click.stop="register = true">Register</v-btn>
        <!-- Login Content -->
          <v-dialog v-model="loginfunc" max-width="500px">
              <v-card>
                <v-card-title>
                  Login
                </v-card-title>
                <v-card-text>
                  <v-form v-model="valid" ref="formLogin" lazy-validation>
                      <v-text-field
                      label="Email" v-model="username" :rules="usernameRules" required></v-text-field>
                      <v-text-field
                      label="Password" v-model="password" :rules="passwordRules" required></v-text-field>
                      <v-radio-group v-model="loginRadio" :mandatory="true">
                        <v-radio label="Booking Agent" value="booking_agent"></v-radio>
                        <v-radio label="Airline Staff" value="airline_staff"></v-radio>
                        <v-radio label="Customer" value="customer"></v-radio>
                      </v-radio-group>
                    <v-btn @click="loginfunction" :disabled="!valid">Login</v-btn>
                  </v-form>
                </v-card-text>
                <v-card-actions>
                  <v-btn color="primary" flat @click.stop="loginfunc=false">Close</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            <!-- Register Content -->
            <v-dialog v-model="register" max-width="500px">
                  <v-card>
                    <v-card-title>
                      Register
                    </v-card-title>
                    <v-card-text>
                      <v-form v-model="valid" ref="formRegister" lazy-validation>
                          <v-text-field
                          label="Email" v-model="username" :rules="usernameRules" required></v-text-field>
                          <v-text-field
                          label="Password" v-model="password" :rules="passwordRules" required></v-text-field>
                          <v-radio-group v-model="signup" :mandatory="true" v-bind:this.radiocheck.sync="this.radiocheck='true'">
                            <v-radio label="Booking Agent" value="booking_agent"></v-radio>
                            <v-radio label="Airline Staff" value="airline_staff"></v-radio>
                            <v-radio label="Customer" value="customer"></v-radio>
                          </v-radio-group>
                          <div v-if="radiocheck" >
                            <div v-if="this.signup=='booking_agent'">
                              <v-text-field
                              label="Booking Agent ID" v-model="booking_agent_id" required></v-text-field>
                            </div>
                            <div v-else-if="this.signup=='airline_staff'">
                              <v-text-field
                              label="First Name" v-model="first_name" required></v-text-field>
                              <v-text-field
                              label="Last Name" v-model="last_name" required></v-text-field>
                              <v-text-field
                              label="Airline Name" v-model="airline_name" required></v-text-field>
                              <v-menu ref="menu2" lazy :close-on-content-click="false" v-model="menu2" transition="scale-transition" offset-y
                                full-width :nudge-right="40" min-width="290px" :return-value.sync="dob">
                                <v-text-field slot="activator" label="Date of Birth" v-model="dob" readonly></v-text-field>
                                <v-date-picker v-model="dob" scrollable>
                                  <v-spacer></v-spacer>
                                  <v-btn flat color="primary" @click="dob = false">Cancel</v-btn>
                                  <v-btn flat color="primary" @click="$refs.menu2.save(dob)">OK</v-btn>
                                </v-date-picker>
                              </v-menu>
                            </div>
                            <div v-else-if="this.signup=='customer'">
                              <v-text-field
                              label="Name" v-model="name" required></v-text-field>
                              <v-text-field
                              label="Building Number" v-model="building_number" required></v-text-field>
                              <v-text-field
                              label="Street" v-model="street" required></v-text-field>
                              <v-text-field
                              label="City" v-model="city" required></v-text-field>
                              <v-text-field
                              label="State" v-model="state" required></v-text-field>
                              <v-text-field
                              label="Phone Number" v-model="phone_number" required></v-text-field>
                              <v-text-field
                              label="Passport Number" v-model="passport_number" required></v-text-field>
                              <v-text-field
                              label="Passport Expiration" v-model="passport_expiration" required></v-text-field>
                              <v-text-field
                               label="Passport Country" v-model="passport_country" required></v-text-field>
                              <v-menu ref="menu1" lazy :close-on-content-click="false" v-model="menu1" transition="scale-transition" offset-y
                                full-width :nudge-right="40" min-width="290px" :return-value.sync="dob">
                                <v-text-field slot="activator" label="Date of Birth" v-model="dob" readonly></v-text-field>
                                <v-date-picker v-model="dob" scrollable>
                                  <v-spacer></v-spacer>
                                  <v-btn flat color="primary" @click="dob = false">Cancel</v-btn>
                                  <v-btn flat color="primary" @click="$refs.menu1.save(dob)">OK</v-btn>
                                </v-date-picker>
                              </v-menu>
                            </div>
                          </div>
                        <v-btn @click="registerfunction" :disabled="!valid">Register</v-btn>
                      </v-form>
                    </v-card-text>
                    <v-card-actions>
                      <v-btn color="primary" flat @click.stop="register=false">Close</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
          </v-flex>
        </v-layout>
      </div>

      <!-- user info/hover menu   -->
      <div v-else>
        <v-layout row wrap justify-end>
          <v-flex xs4>
          <!-- menu dropdown -->
            <v-menu offset-y>
              <v-btn color="primary" dark slot="activator">User Name</v-btn>
              <v-list>
                <v-list-tile v-for="item in dropdown" :key="item.title" @click="dropdownMenu(item.title)">
                  <v-list-tile-title>{{ item.title }}</v-list-tile-title>
                </v-list-tile>
              </v-list>
            </v-menu>
          </v-flex>
        </v-layout>
      </div>


    <router-view/>
  </v-app>
  </div>
</template>

<script>
import axios from 'axios'
import 'vuetify/dist/vuetify.min.css'
import Vue from 'vue'

export default {
  name: 'app',
  data (){
    return {
      e1: 'recent',
      valid: true,
      radiocheck: false, //toggle for type of registration
      login: false, //to toggle for menu
      loginfunc: false, //for form
      register: false, //for form
      signup: '', //value of radio will be sent here when radio checked
      loginRadio: '', //value of radio for login
      username: '',
      usernameRules: [v => !!v || 'username is required'],
      password: '',
      passwordRules: [v => !!v || 'password is required'],
      dropdown: [
        {title: 'My Bookings'},
        {title: 'Track Spending'},
        {title: 'Statistics'},
        {title: 'Forms'},
        {title: 'Logout'}
      ],
      name: null,
      building_number: null,
      street: null,
      city: null,
      state: null,
      phone_number: null,
      passport_number: null,
      passport_expiration: null,
      passport_country: null,
      dob: null,
      menu1: false, //menu for dob picker
      first_name: null,
      last_name: null,
      airline_name:null,
      menu2: false,
      booking_agent_id: null,

    }
  },
  created () {
    // this.login = true
    this.getSessionVars()
    if (this.$login != null) {
      this.login= true
    }
  },
  methods: {
    router (item) {
      console.log("router item",item);
      if (item ==  'home') {
        window.location.replace('http://localhost:8000')
      }
    },
    loginfunction() {
      console.log('testing login', this.username, "+ ", this.password)
      const path = `http://localhost:5000/login/auth`;
      Vue.prototype.$login = 'airline_staff' //for testing
      console.log("$login", this.$login);
      this.changeDropdown() //testing
      // this.login = true
      var d = {"email":this.username, "password":this.password, "typ":this.loginRadio};
      axios.post(path,d)
        .then(response => {
          var res = response.data;
          console.log(res);
          this.login = true //change this.login = true for menu
          this.getSessionVars()
          this.changeDropdown()//since login worked, call function to change dropdown
        })
        .catch(error => {
          console.log('login -->', error);
        });
    },
    registerfunction(item) {
      const path = `http://localhost:5000/register/auth`;
      var d = {'email': this.username,
        'password': this.password,
        'typ': this.signup,
        'name': this.name,
        'building_number': this.building_number,
        'street': this.street,
        'city': this.city,
        'state': this.state,
        'phone_number': this.phone_number,
        'passport_number': this.passport_number,
        'passport_expiration': this.passport_expiration,
        'passport_country': this.passport_country,
        'dob': this.dob,
        'first_name': this.first_name,
        'last_name': this.last_name,
        'airline_name': this.airline_name,
        'booking_agent_id': this.booking_agent_id};
      //todo: add fields to registration
      axios.post(path,d)
        .then(response => {
          var res = response.data;
          console.log(res);
          this.login = true //change this.login = true for menu
          this.getSessionVars()
          this.changeDropdown() //since register worked, call function to change dropdown
        })
        .catch(error => {
          console.log('login -->', error);
        });
    },
    getSessionVars() {
      const path = `http://localhost:5000/session/vars`;
      axios.post(path)
        .then(response => {
          let res = response.data;
          console.log("res" ,res);
          Vue.prototype.$login = res
        })
        .catch(error => {
          console.log('getting session vars-->', error);
        });
    },
    changeDropdown() { //where dropdown btns will be shown
      if (this.$login == 'customer') {
        this.dropdown = [
          {title: 'My Bookings'},
          {title: 'Track Spending'},
          {title: 'Logout'}
        ]
      }
      if (this.$login == 'booking_agent') {
        this.dropdown = [
          {title: 'Bookings'},
          {title: 'Statistics'},
          {title: 'Logout'}
        ]
      }
      if (this.$login == 'airline_staff') {
        this.dropdown = [
          {title: 'Bookings/Flights'},
          {title: 'Statistics'},
          {title: 'Forms'},
          {title: 'Logout'}
        ]
      }
      this.login = true //login worked, so change menu
    },
    dropdownMenu (item) {
      console.log("item",item);
      if (item == "Logout") {
        const path = `http://localhost:5000/logout/auth`
        var d = {
          "user_logout": true,
        }
        axios.post(path, d)
          .then (response => {
            $this.$swal(
              `You Logged Out`,
              'success'
            )
            window.location.replace('http://localhost:8000/')
          })
      }
      if (item == "Forms") {
        window.location.replace('http://localhost:8000/forms')
      }
      if (item == "My Bookings") {
        window.location.replace('http://localhost:8000/bookings')
      }
      if (item == "Track Spending") {
        window.location.replace('http://localhost:8000/spending')
      }
      if (item == "Statistics") {
        window.location.replace('http://localhost:8000/statistics')
      }
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
