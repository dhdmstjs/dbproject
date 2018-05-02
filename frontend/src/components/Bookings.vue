<template>
  <div>
    <v-app>
    <v-layout row wrap justify-center>
      <v-flex xs12 >
        <h1>Bookings</h1><br>

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
                <td class="text-xs-right">{{ props.item.departure_airpot }}</td>
                <td class="text-xs-right">{{ props.item.arrival_city }}</td>
                <td class="text-xs-right">{{ props.item.arrival_airport }}</td>
                <td class="text-xs-right">{{ props.item.datesResult }}</td>
                <td class="text-xs-right">{{ props.item.price }}</td>
                <td class="text-xs-right">{{ props.item.status }}</td>
              </template>
            <template slot="no-data">
              <v-btn color="primary" @click="initialize">Reset</v-btn>
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
                <td class="text-xs-right">{{ props.item.departure_airpot }}</td>
                <td class="text-xs-right">{{ props.item.arrival_city }}</td>
                <td class="text-xs-right">{{ props.item.arrival_airport }}</td>
                <td class="text-xs-right">{{ props.item.datesResult }}</td>
                <td class="text-xs-right">{{ props.item.price }}</td>
                <td class="text-xs-right">{{ props.item.status }}</td>
              </template>

            <template slot="no-data">
              <v-btn color="primary" @click="initialize">Reset</v-btn>
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
                <td class="text-xs-right">{{ props.item.departure_airpot }}</td>
                <td class="text-xs-right">{{ props.item.arrival_airport }}</td>
                <td class="text-xs-right">{{ props.item.datesResult }}</td>
                <td class="text-xs-right">{{ props.item.status }}</td>
              </template>
            <template slot="no-data">
              <v-btn color="primary" @click="initialize">Reset</v-btn>
            </template>
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
                          <td class="text-xs-right">{{ props.item.departure_airpot }}</td>
                          <td class="text-xs-right">{{ props.item.arrival_airport }}</td>
                          <td class="text-xs-right">{{ props.item.datesResult }}</td>
                          <td class="text-xs-right">{{ props.item.status }}</td>
                        </tr>
                      </template>
                      <template slot="expand" slot-scope="props">
                        <v-card flat>
                          <v-card-text>Customers: list all customer emails here for that flight</v-card-text>
                        </v-card>
                      </template>
                    <template slot="no-data">
                      <v-btn color="primary" @click="initialize">Reset</v-btn>
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
        { text: 'Arrival City', value: 'arrival_city' },
        { text: 'Arrival Airport', value: 'arrival_airport' },
        { text: 'Date', value: 'datesResult', sortable: false },
        { text: 'Price', value: 'price' },
        { text: 'Status', value: 'status' },
      ],
      headers_booking: [
        { text: 'Customer', value: 'customer_email' },
        { text: 'Airline', value: 'airline_name' },
        { text: 'Flight Number', value: 'flight_num' },
        { text: 'Departure City', value: 'departure_city' },
        { text: 'Departure Airport', value: 'departure_airport' },
        { text: 'Arrival City', value: 'arrival_city' },
        { text: 'Arrival Airport', value: 'arrival_airport' },
        { text: 'Date', value: 'datesResult', sortable: false },
        { text: 'Price', value: 'price' },
        { text: 'Status', value: 'status' },
      ],
      headers_airline: [
          { text: 'Flight Number', value: 'flight_num' },
          { text: 'Departure Airport', value: 'departure_airport' },
          { text: 'Arrival Airport', value: 'arrival_airport' },
          { text: 'Date', value: 'datesResult', sortable: false },
          { text: 'Status', value: 'status' },
        ],
      headers_results: [
          { text: 'Flight Number', value: 'flight_num' },
          { text: 'Departure Airport', value: 'departure_airport' },
          { text: 'Arrival Airport', value: 'arrival_airport' },
          { text: 'Date', value: 'datesResult', sortable: false },
          { text: 'Status', value: 'status' },
        ],
    }
  },
  created () {
    this.$login = 'airline_staff'
    console.log("this", this.$login);
    this.initialize()
    //call from db type of login
    //this.$login = ''
  },
  methods: {
    submit (){
      if (this.$refs.form.validate()) { //search flights
        this.showFlights = true
      }
    },
    clear () {
      this.$refs.form.reset()
    },
    initialize () {
      this.items_customer = [
        {
          airline_name: 'hello',
          flight_num: 123,
          departure_city: 'Frozen Yogurt',
          departure_airpot: 159,
          arrival_city: 6.0,
          arrival_airport: 24,
          datesResult: 4.0,
          price: 12345,
          status: 'hihi'

        },
        {
          airline_name: 'hello',
          flight_num: 123,
          departure_city: 'Ice cream sandwich',
          departure_airpot: 237,
          arrival_city: 9.0,
          arrival_airport: 37,
          datesResult: 4.3,
          price: 12345,
          status: 'hihi'
        }
      ]
      this.items_airline = [
        {
          airline_name: 'hello',
          flight_num: 123,
          departure_city: 'Frozen Yogurt',
          departure_airpot: 159,
          arrival_city: 6.0,
          arrival_airport: 24,
          datesResult: 4.0,
          price: 12345,
          status: 'hihi'

        },
        {
          airline_name: 'hello',
          flight_num: 123,
          departure_city: 'Ice cream sandwich',
          departure_airpot: 237,
          arrival_city: 9.0,
          arrival_airport: 37,
          datesResult: 4.3,
          price: 12345,
          status: 'hihi'
        }
      ]
      this.items_results = [
        {
          airline_name: 'hello',
          flight_num: 1234,
          departure_city: 'Frozen Yogurt',
          departure_airpot: 159,
          arrival_city: 6.0,
          arrival_airport: 24,
          datesResult: 4.0,
          price: 12345,
          status: 'hihi'

        },
        {
          airline_name: 'hello',
          flight_num: 123,
          departure_city: 'Ice cream sandwich',
          departure_airpot: 237,
          arrival_city: 9.0,
          arrival_airport: 37,
          datesResult: 4.3,
          price: 12345,
          status: 'hihi'
        }
      ]
    },

  }
}
</script>

<style scoped>

</style>
