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
    <div class = "dtable" v-if="this.submitbtn==true">
      <v-data-table
        :headers="headers"
        :items="items"
        hide-actions
        class="elevation-1">
        <template slot="items" slot-scope="props">
          <td class="text-xs-right">{{ props.item.departure_city }}</td>
          <td class="text-xs-right">{{ props.item.departure_airpot }}</td>
          <td class="text-xs-right">{{ props.item.arrival_city }}</td>
          <td class="text-xs-right">{{ props.item.arrival_airport }}</td>
          <td class="text-xs-right">{{ props.item.datesResult }}</td>
          <td class="text-xs-right">{{ props.item.airline_name }}</td>
          <td class="text-xs-right">{{ props.item.flight_num }}</td>
          <td class="text-xs-right">{{ props.item.price }}</td>
          <td class="justify-center layout px-0">
            <v-btn icon class="mx-0" @click="buyItem(props.item)">
              <v-icon color="pink">add</v-icon>
            </v-btn>
          </td>
        </template>
        <template slot="no-data">
          <v-btn color="primary" @click="initialize">Reset</v-btn>
        </template>
      </v-data-table>
    </div>
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
        { text: 'Departure City', value: 'departure_city' },
        { text: 'Departure Airport', value: 'departure_airport' },
        { text: 'Arrival City', value: 'arrival_city' },
        { text: 'Arrival Airport', value: 'arrival_airport' },
        { text: 'Date', value: 'datesResult', sortable: false },
        { text: 'Airline', value: 'airline_name' },
        { text: 'Flight Number', value: 'flight_num' },
        { text: 'Price', value: 'price' },
        { text: 'Buy', value: 'buyitem' },
      ],
     items: [],
     submitbtn: false, //toggle for table add it to after axios response
    }
  },
  created () {
    this.$login = 'customer'
    this.initialize()
  },
  methods: {
    submit () {
      this.submitbtn = true
      console.log("thisRef", this.$refs.form.validate());
      console.log("thisRef", this.$refs.form2.validate());

      if (this.$refs.form.validate()) { //search flights
        console.log("this.depart",this.depart);
        console.log("this.arrive",this.arrive);
        console.log("this.date",this.date);
        const path = `http://localhost:5000/api/getflights`;
        var d = {"depart":this.depart,"arrive":this.arrive,"date":this.date};
        axios.post(path,d)
          .then(response => {
            var res = response.data;
            console.log(res);
          })
          .catch(error => {
            console.log('getting flights -->', error);
          });
      }

      if (this.$refs.form2.validate()) { //check flight status
        console.log("this.depart",this.flight_num);
        console.log("this.arrive",this.date2);
        const path = `http://localhost:5000/api/getflights`;
        var d = {"flight_num":this.flight_num,"date":this.date2};
        axios.post(path,d)
          .then(response => {
            var res = response.data;
            console.log(res);
            // update table with this data
            //this.items = res.whateverthing
          })
          .catch(error => {
            console.log('getting flights -->', error);
          });
      }
    },
    clear () {
      this.$refs.form.reset()
    },
    buyItem (item) {
      const index = this.items.indexOf(item);
      console.log("item",item);
      let val = confirm('Are you sure you want to buy this item?')
      console.log("this.$login", this.$login);
      if (this.$login == null && val == true) { //user hasn't logged in && wants to buy
        console.log("hellonull");
        confirm('Make sure to log in first')
      }
      if (this.$login == 'customer' && val == true) { // wants to buy ticket
        console.log("val",val);
        var d = {"airline_name": item.airline_name, "flight_num": this.flight_num}
        //send airline_name && flight_num
        const path = `http://localhost:5000/api/???`; //change path
        axios.post(path,d)
          .then(response => {
            var res = response.data; //data sent from server
            console.log(res);
            //if res == yes then add flight to customer, else don't
          })
          .catch(error => {
            console.log('getting flights -->', error);
          });

      }
      if (this.$login == 'booking_agent' && val == true) { // wants to buy ticket
        console.log("val",val);
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
      var d = {"airline_name": item.airline_name, "flight_num": this.flight_num, "cutomer_email": this.cust_email_dialog}
      //send airline_name && flight_num
      const path = `http://localhost:5000/api/???`; //change path
      axios.post(path,d)
        .then(response => {
          var res = response.data; //data sent from server
          console.log(res);
          //if res == yes then add flight to customer, else don't
        })
        .catch(error => {
          console.log('getting flights -->', error);
        });

    },
    initialize () {
      this.items = [
        {
          departure_city: 'Frozen Yogurt',
          departure_airpot: 159,
          arrival_city: 6.0,
          arrival_airport: 24,
          datesResult: 4.0,
          airline_name: 'hello',
          flight_num: 123,
          price: 12345

        },
        {
          departure_city: 'Ice cream sandwich',
          departure_airpot: 237,
          arrival_city: 9.0,
          arrival_airport: 37,
          datesResult: 4.3,
          airline_name: 'hello',
          flight_num: 123,
          price: 12345

        },
        {
          departure_city: 'Eclair',
          departure_airpot: 262,
          arrival_city: 16.0,
          arrival_airport: 23,
          datesResult: 6.0,
          airline_name: 'hello',
          flight_num: 123,
          price: 12345

        },
        {
          departure_city: 'Cupcake',
          departure_airpot: 305,
          arrival_city: 3.7,
          arrival_airport: 67,
          datesResult: 4.3,
          airline_name: 'hello',
          flight_num: 123,
          price: 12345

        },
        {
          departure_city: 'Gingerbread',
          departure_airpot: 356,
          arrival_city: 16.0,
          arrival_airport: 49,
          datesResult: 3.9,
          airline_name: 'hello',
          flight_num: 123,
          price: 12345
        }
      ]
    },

  }
}
</script>

<style scoped>


</style>
