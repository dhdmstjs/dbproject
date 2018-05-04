airport<template>
  <div>
    <v-app>
    <v-layout row wrap justify-center>
      <v-flex xs12 >
        <h1>Upcoming Flights</h1><br>

        <div v-if="this.$login=='customer'">
          <v-data-table
            :headers="headers_customer"
            :items="items_customer"
            hide-actions
            class="elevation-1">
              <template slot="items" slot-scope="props">
                <td class="text-xs-right">{{ props.item.airline_name }}</td>
                <td class="text-xs-right">{{ props.item.flight_num }}</td>
                <td class="text-xs-right">{{ props.item.departure_city }}</td>
                <td class="text-xs-right">{{ props.item.departure_airport }}</td>
                <td class="text-xs-right">{{ props.item.arrival_city }}</td>
                <td class="text-xs-right">{{ props.item.arrival_airport }}</td>
                <td class="text-xs-right">{{ props.item.datesResult }}</td>
                <td class="text-xs-right">{{ props.item.price }}</td>
                <td class="text-xs-right">{{ props.item.status }}</td>
              </template>

          </v-data-table>
        </div>

        <div v-else-if="this.$login=='booking_agent'">
          <v-data-table
            :headers="headers_booking"
            :items="items_booking"
            hide-actions
            class="elevation-1">
              <template slot="items" slot-scope="props">
                <td class="text-xs-right">{{ props.item.customer_email }}</td>
                <td class="text-xs-right">{{ props.item.airline_name }}</td>
                <td class="text-xs-right">{{ props.item.flight_num }}</td>
                <td class="text-xs-right">{{ props.item.departure_city }}</td>
                <td class="text-xs-right">{{ props.item.departure_airport }}</td>
                <td class="text-xs-right">{{ props.item.departure_time }}</td>
                <td class="text-xs-right">{{ props.item.arrival_city }}</td>
                <td class="text-xs-right">{{ props.item.arrival_airport }}</td>
                <td class="text-xs-right">{{ props.item.arrival_time }}</td>
                <td class="text-xs-right">{{ props.item.price }}</td>
                <td class="text-xs-right">{{ props.item.status }}</td>
              </template>


          </v-data-table>
        </div>

        <div v-else-if="this.$login=='airline_staff'">
          <v-data-table
            :headers="headers_airline"
            :items="items_airline"
            hide-actions
            class="elevation-1">
              <template slot="items" slot-scope="props">
                <td class="text-xs-right">{{ props.item.flight_num }}</td>
                <td class="text-xs-right">{{ props.item.departure_airport }}</td>
                <td class="text-xs-right">{{ props.item.departure_time }}</td>

                <td class="text-xs-right">{{ props.item.arrival_airport }}</td>
                <td class="text-xs-right">{{ props.item.arrival_time }}</td>
                <td class="text-xs-right">{{ props.item.status }}</td>
              </template>
            <!-- <template slot="no-data">
              <v-btn color="primary" @click="initialize">Reset</v-btn>
            </template> -->
          </v-data-table>
          <br><br><br>

          <v-card>
            <v-layout row wrap justify-center>
              <v-flex xs7>
                <br>
                <h2> Search for all flights </h2>
                <v-form v-model="valid" ref="form" lazy-validation>
                    <v-text-field
                    label="Depart From" v-model="departure" required></v-text-field>
                    <v-text-field
                    label="Arrive At" v-model="arrival" required></v-text-field>
                      <v-menu ref="menu1" lazy :close-on-content-click="false" v-model="menu1" transition="scale-transition" offset-y
                        full-width :nudge-right="40" min-width="290px" :return-value.sync="date1">
                        <v-text-field slot="activator" label="Start Date" v-model="date1" readonly></v-text-field>
                        <v-date-picker v-model="date1" no-title scrollable>
                          <v-spacer></v-spacer>
                          <v-btn flat color="primary" @click="menu1 = false">Cancel</v-btn>
                          <v-btn flat color="primary" @click="$refs.menu1.save(date1)">OK</v-btn>
                        </v-date-picker>
                      </v-menu>
                    <br>
                    <v-menu ref="menu2" lazy :close-on-content-click="false" v-model="menu2" transition="scale-transition" offset-y
                      full-width :nudge-right="40" min-width="290px" :return-value.sync="date2">
                      <v-text-field slot="activator" label="End Date" v-model="date2" readonly></v-text-field>
                      <v-date-picker v-model="date2" no-title scrollable>
                        <v-spacer></v-spacer>
                        <v-btn flat color="primary" @click="menu2 = false">Cancel</v-btn>
                        <v-btn flat color="primary" @click="$refs.menu2.save(date2)">OK</v-btn>
                      </v-date-picker>
                    </v-menu>
                  <v-btn @click="submit" :disabled="!valid">submit</v-btn>
                  <v-btn @click="clear">clear</v-btn>
                  <br><br>
                </v-form>

                <div v-if="showFlights">
                  <v-data-table
                    :headers="headers_results"
                    :items="items_results"
                    item-key="flight_num"
                    hide-actions
                    class="elevation-1">
                      <template slot="items" slot-scope="props">
                        <tr @click="props.expanded = !props.expanded">
                          <td class="text-xs-right">{{ props.item.flight_num }}</td>
                          <td class="text-xs-right">{{ props.item.departure_airport }}</td>
                          <td class="text-xs-right">{{ props.item.departure_time }}</td>

                          <td class="text-xs-right">{{ props.item.arrival_airport }}</td>
                          <td class="text-xs-right">{{ props.item.arrival_time }}</td>

                          <td class="text-xs-right">{{ props.item.status }}</td>
                        </tr>
                      </template>
                      <template slot="expand" slot-scope="props">
                        <v-card flat>
                          <v-card-text>Customers: list all customer emails here for that flight</v-card-text>
                          <!-- {{props.item.customers}} -->
                        </v-card>
                      </template>
                  </v-data-table>
                </div>
                <br><br><br>
              </v-flex>
            </v-layout>
          </v-card>


        </div>

      </v-flex>
    </v-layout>
  </v-app>
  </div>
</template>

<script>
import axios from 'axios'
import 'vuetify/dist/vuetify.min.css'

export default {
  data () {
    return {
      valid: true,
      items_customer: [],
      items_booking: [],
      items_airline: [],
      items: [], //for airline staff search data
      menu1: false,
      menu2: false,
      date1: null, //start date
      date2: null, //end date
      showFlights: false,
      departure: null, //departure input from airline staff
      arrival: null, //arrival input from airline staff
      headers_customer: [
        { text: 'Airline', value: 'airline_name' },
        { text: 'Flight Number', value: 'flight_num' },
        { text: 'Departure City', value: 'departure_city' },
        { text: 'Departure Airport', value: 'departure_airport' },
        { text: 'Departure Time', value: 'departure_time' },

        { text: 'Arrival City', value: 'arrival_city' },
        { text: 'Arrival Airport', value: 'arrival_airport' },
        { text: 'Arrival Time', value: 'arrival_time' },

        { text: 'Price', value: 'price' },
        { text: 'Status', value: 'status' },
      ],
      headers_booking: [
        { text: 'Customer', value: 'customer_email' },
        { text: 'Airline', value: 'airline_name' },
        { text: 'Flight Number', value: 'flight_num' },
        { text: 'Departure City', value: 'departure_city' },
        { text: 'Departure Airport', value: 'departure_airport' },
        { text: 'Departure Time', value: 'departure_time' },

        { text: 'Arrival City', value: 'arrival_city' },
        { text: 'Arrival Airport', value: 'arrival_airport' },
        { text: 'Arrival Time', value: 'arrival_time' },

        { text: 'Price', value: 'price' },
        { text: 'Status', value: 'status' },
      ],
      headers_airline: [
          { text: 'Flight Number', value: 'flight_num' },
          { text: 'Departure Airport', value: 'departure_airport' },
          { text: 'Departure Time', value: 'departure_time' },
          { text: 'Arrival Airport', value: 'arrival_airport' },
          { text: 'Arrival Time', value: 'arrival_time' },
          { text: 'Status', value: 'status' },
        ],
      headers_results: [
          { text: 'Flight Number', value: 'flight_num' },
          { text: 'Departure Airport', value: 'departure_airport' },
          { text: 'Departure Time', value: 'departure_time' },
          { text: 'Arrival Airport', value: 'arrival_airport' },
          { text: 'Arrival Time', value: 'arrival_time' },
          { text: 'Status', value: 'status' },
        ],

    }
  },
  created () {
    this.$login = 'airline_staff'
    // this.$login = 'booking_agent'
    // this.$login = 'customer'

    console.log("this", this.$login);
    //call from db type of login
    //this.$login = ''
    // this.callData() //calls data for bookings
  },
  methods: {
    callData(){
      const path = `http://localhost:5000/api/####`
      var d = {
        "login_type": this.$login,
        "page_type": "bookings"
      }
      axios.post(path, d)
        .then(response => {
          var res = response.data //give me login_usertype,
          console.log(res);
          if (res.login_usertype == 'customer') {
            //this.items_customer = res.dataitems
          }
          if (res.login_usertype == 'booking_agent') {
            //this.items_booking = res.dataitems
          }
          if (res.login_usertype == 'airline_staff') {
            //this.items_airline = res.dataitems
          }
        })
        .catch(error => {
          console.log("error changing status");
        })
    },
    submit (){
      if (this.$refs.form.validate()) { //search flights for staff
        this.showFlights = true
        const path = `http://localhost:5000/api/getflights`
        var d = {
          "departure": this.departure,
          "arrival": this.arrival,
          "departure_time": this.date1,
          "arrival_time": this.date2
        }
        axios.post(path, d)
          .then(response => {
            var res = response.data //return flights
            console.log(res);
            //this.items = res.dataitems
          })
          .catch(error => {
            console.log("error getting flights");
          })
      }
    },
    clear () {
      this.$refs.form.reset()
    },

  }
}
</script>

<style scoped>

</style>
