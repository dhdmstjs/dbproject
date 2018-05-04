<template>
  <div>
    <v-app>
    <!-- <p>Random number from backend: {{ randomNumber }}</p>
    <button @click="getRandom">New random number</button> -->

      <br><br><br><br><br><br>
      <v-layout row wrap justify-center>
        <v-flex xs5>
        <v-tabs centered v-model="tabs" color="cyan" dark slider-color="yellow">
            <v-tab ripple>
              Search for Flights
            </v-tab>
            <v-tab ripple>
              Check Flight Status
            </v-tab>
            <v-tab-item >
              <v-layout row wrap justify-center>
                <v-flex xs7>
                  <br><h2> Search for Flights</h2>
                  <v-form v-model="valid" ref="form" lazy-validation>
                      <v-text-field
                      label="Depart From" v-model="depart" :rules="departRules" required></v-text-field>
                      <v-text-field
                      label="Arrive At" v-model="arrive" :rules="arriveRules" required></v-text-field>
                          <v-menu ref="menu" lazy :close-on-content-click="false" v-model="menu" transition="scale-transition" offset-y
                            full-width :nudge-right="40" min-width="290px" :return-value.sync="date">
                            <v-text-field slot="activator" label="Depart Date" v-model="date" readonly></v-text-field>
                            <v-date-picker v-model="date" no-title scrollable>
                              <v-spacer></v-spacer>
                              <v-btn flat color="primary" @click="menu = false">Cancel</v-btn>
                              <v-btn flat color="primary" @click="$refs.menu.save(date)">OK</v-btn>
                            </v-date-picker>
                          </v-menu>
                      <br>
                    <v-btn @click="submit" :disabled="!valid">submit</v-btn>
                    <v-btn @click="clear">clear</v-btn>
                  </v-form>
                </v-flex>
              </v-layout>

            </v-tab-item>

            <v-tab-item >
              <v-layout row wrap justify-center>
                <v-flex xs7>
                  <br><h2> Check Status</h2>
                  <v-form v-model="valid" ref="form2" lazy-validation>
                      <v-text-field
                      label="Flight Number" v-model="flight_num" :rules="flightnumRules" required></v-text-field>
                          <v-menu
                            ref="menu2" lazy :close-on-content-click="false" v-model="menu2" transition="scale-transition" offset-y
                            full-width :nudge-right="40" min-width="290px" :return-value.sync="date2">
                            <v-text-field slot="activator" label="Depart / Arrive Date" v-model="date2" readonly></v-text-field>
                            <v-date-picker v-model="date2" no-title scrollable>
                              <v-spacer></v-spacer>
                              <v-btn flat color="primary" @click="menu2 = false">Cancel</v-btn>
                              <v-btn flat color="primary" @click="$refs.menu2.save(date2)">OK</v-btn>
                            </v-date-picker>
                          </v-menu>
                      <br>
                    <v-btn @click="submit" :disabled="!valid">submit</v-btn>
                    <v-btn @click="clear">clear</v-btn>
                  </v-form>
                </v-flex>
              </v-layout>

            </v-tab-item>
          </v-tabs>
        </v-flex>
      </v-layout>


<!-- data table -->
<v-layout row wrap justify-center>
    <div class = "dtable" v-if="this.submitbtn==true">
      <v-data-table :headers="headers" :items="items" hide-actions class="elevation-1">
        <template slot="items" slot-scope="props">
          <!-- <td class="text-xs-right">{{ props.item.departure_city }}</td> -->
          <td class="text-xs-center">{{ props.item.departure_airport }}</td>
          <td class="text-xs-center">{{ props.item.departure_time }}</td>

          <!-- <td class="text-xs-right">{{ props.item.arrival_city }}</td> -->
          <td class="text-xs-center">{{ props.item.arrival_airport }}</td>
          <td class="text-xs-center">{{ props.item.arrival_time }}</td>

          <td class="text-xs-center">{{ props.item.airline_name }}</td>
          <td class="text-xs-center">{{ props.item.flight_num }}</td>
          <td class="text-xs-center">{{ props.item.price }}</td>
          <td class="justify-center layout px-0">
            <v-btn icon class="mx-0" @click="buyItem(props.item)">
              <v-icon color="pink">add</v-icon>
            </v-btn>
          </td>
        </template>
        <!-- <template slot="no-data">
          <v-btn color="primary" @click="initialize">Reset</v-btn>
        </template> -->
      </v-data-table>
    </div>
</v-layout>

    <!-- will only open if booking agent buying ticket -->
    <div v-if="opendialog">
      <v-dialog v-model="dialog" max-width="500px">
          <v-card>
            <v-card-title>
              Input customer email
            </v-card-title>
            <v-form v-model="valid" ref="formE" lazy-validation>
              <v-text-field
                label="Customer Email" v-model="cust_email_dialog" required></v-text-field>
              <v-card-actions>
                <v-btn @click="submitE" :disabled="!valid">submit</v-btn>
                <v-btn color="primary" flat @click.stop="dialog=false">Close</v-btn>
              </v-card-actions>
            </v-form>

          </v-card>
        </v-dialog>
      </div>

  </v-app>
  </div>
</template>

<script>
import axios from 'axios'
import 'vuetify/dist/vuetify.min.css'

export default {
  data () {
    return {
      opendialog: false, //flag to open dialog for booking agent to buy ticket
      dialog: false,
      cust_email_dialog:null,
      randomNumber: 0,
      tabs: null,
      date: null,
      date2: null, //for check flight status
      menu: false,
      menu2:false,
      valid: true,
      depart: '',
      departRules: [v => !!v || 'Depart City is required'],
      arrive: '',
      arriveRules: [v => !!v || 'Depart City is required'],
      flight_num: '',
      flightnumRules: [v => !!v || 'Depart City is required'],
      headers: [
        // { text: 'Departure City', value: 'departure_city' },
        { text: 'Departure Airport', value: 'departure_airport' },
        { text: 'Departure Time', value: 'departure_time', sortable: false },

        // { text: 'Arrival City', value: 'arrival_city' },
        { text: 'Arrival Airport', value: 'arrival_airport' },
        { text: 'Arrival Time', value: 'arrival_time', sortable: false },

        { text: 'Airline', value: 'airline_name', sortable: false },
        { text: 'Flight Number', value: 'flight_num', sortable: false },
        { text: 'Price', value: 'price' },
        { text: 'Buy', value: 'buyitem' },
      ],
      items: [],
      submitbtn: false, //toggle for table add it to after axios response
      session: '',
    }
  },
  created () {
    this.$login = 'customer'
  },
  methods: {
    submit() {
      this.submitbtn = true
      console.log("thisRef", this.$refs.form.validate());
      console.log("thisRef", this.$refs.form2.validate());

      if (this.$refs.form.validate()) { //search flights
        console.log("this.depart", this.depart);
        console.log("this.arrive", this.arrive);
        console.log("this.date", this.date);
        const path = `http://localhost:5000/api/getflights`;
        var d = {"depart": this.depart, "arrive": this.arrive, "date": this.date};
        axios.post(path, d)
          .then(response => {
            var res = response.data;
            this.items = res;
            console.log("reponse", this.items);
          })
          .catch(error => {
            console.log('getting flights -->', error);
          });
      }

      if (this.$refs.form2.validate()) { //check flight status
        console.log("this.depart", this.flight_num);
        console.log("this.arrive", this.date2);
        const path = `http://localhost:5000/api/getflights`;
        var d = {"flight_num": this.flight_num, "date": this.date2};
        axios.post(path, d)
          .then(response => {
            var res = response.data;
            console.log(res);
            // update table with this data
            this.items = res
          })
          .catch(error => {
            console.log('getting flights -->', error);
          });
      }
    },
    clear() {
      console.log(this.getSessionVars());
      this.$refs.form.reset()
    },
    buyItem(item) {
      const index = this.items.indexOf(item);
      console.log("item", item);
      let val = confirm('Are you sure you want to buy this item?')
      console.log("this.$login", this.$login);
      if (this.$login == null && val == true) { //user hasn't logged in && wants to buy
        console.log("hellonull");
        confirm('Make sure to log in first')
      }
      if (this.$login == 'customer' && val == true) { // wants to buy ticket
        console.log("val", val);
        var d = {"airline_name": item.airline_name, "flight_num": item.flight_num};
        //send airline_name && flight_num
        const path = `http://localhost:5000/purchase/ticket`; //change path
        const $this = this
        axios.post(path, d)
          .then(response => {
            var res = response.data; //data sent from server
            console.log("response ", res);
            //if res == yes then add flight to customer, else don't
            if (res.success=='false') {
              $this.$swal({
                title: 'Error',
                text: res.message,
                type: 'warning',
              })
            } else if (res.success='true'){
              $this.$swal(
                'Great!',
                `You have bought the ticket~`,
                'success'
              )
            }
          })
          .catch(error => {
            console.log('getting flights -->', error);
            $this.$swal({
              title: 'Error',
              text: "Please try again",
              type: 'warning',
            })

          });

      }
      if (this.$login == 'booking_agent' && val == true) { // wants to buy ticket
        console.log("val", val);
        this.opendialog = true
        this.dialog = true
        this.buyItemCustomer(val)

      }
    },
    submitE() { //for customer email submission
      console.log("this.cust", this.cust_email_dialog);
      this.dialog = false
    },
    buyItemCustomer(item) {
      let email = this.cust_email_dialog
      console.log("email", email);
      var d = {
        "airline_name": item.airline_name,
        "flight_num": item.flight_num,
        "cutomer_email": this.cust_email_dialog
      }
      //send airline_name && flight_num
      const path = `http://localhost:5000/purchase/ticket`; //change path
      axios.post(path, d)
        .then(response => {
          var res = response.data; //data sent from server
          console.log(res);
          //if res == yes then add flight to customer + booking agent, else don't
          $this.$swal(
            `You have bought the ticket~`,
            'success'
          )
        })
        .catch(error => {
          console.log('getting flights -->', error);
          $this.$swal({
            title: 'Error',
            text: "Please try again",
            type: 'warning',
          })
        });

    },
    getSessionVars() {
      const path = `http://localhost:5000/session/vars`;
      axios.post(path)
        .then(response => {
          let res = response.data;
          console.log("res" ,res);
          this.session = res
        })
        .catch(error => {
          console.log('getting session vars-->', error);
        });
    },
  }
}
</script>

<style scoped>


</style>
