<template>
  <div>
    <v-app> <br><br>
      <div v-if="this.$login=='booking_agent'">

          <h2>Commission Data</h2> <v-btn flat color="primary" @click="dateChange">Change date range</v-btn>

                <!-- Data Table -->
            <v-layout row wrap justify-center>
              <v-flex xs8 >
                <v-data-table :headers="headers_commission" :items="items_commission" hide-actions class="elevation-1">
                  <template slot="items" slot-scope="props">
                    <!-- <td class="text-xs-right">{{ props.item.departure_city }}</td> -->
                    <td class="text-xs-center">{{ props.item.totalamount }}</td>
                    <td class="text-xs-center">{{ props.item.average }}</td>
                    <td class="text-xs-center">{{ props.item.totalnumber }}</td>
                  </template>
                </v-data-table>
              </v-flex>
            </v-layout>
            <br><br><br>
        <!-- these dates are to choose date-->
          <div v-if="this.dateRange==true">
            <h2> Choose date range to specify commission data </h2>
            <v-form v-model="valid" ref="form1" lazy-validation>
            <v-layout row wrap justify-center>
              <v-flex xs3 >
                  <v-menu ref="menu1" lazy :close-on-content-click="false" v-model="menu1" transition="scale-transition" offset-y
                    full-width :nudge-right="40" min-width="290px" :return-value.sync="date1">
                    <v-text-field slot="activator" label="Start Date" v-model="date1" readonly></v-text-field>
                    <v-date-picker v-model="date1" no-title scrollable>
                      <v-spacer></v-spacer>
                      <v-btn flat color="primary" @click="menu1 = false">Cancel</v-btn>
                      <v-btn flat color="primary" @click="$refs.menu1.save(date1)">OK</v-btn>
                    </v-date-picker>
                  </v-menu>
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
              </v-flex>
            </v-layout>
          </v-form>
        </div>

        <h2> View Top Customers </h2>
        <v-layout row wrap justify-center>
          <v-flex xs8 >
            <v-data-table :headers="headers_customers" :items="items_customers" hide-actions class="elevation-1">
              <template slot="items" slot-scope="props">
                <td class="text-xs-center">{{ props.item.customer_email }}</td>
                <td class="text-xs-center">{{ props.item.numbertickets }}</td>
                <td class="text-xs-center">{{ props.item.amountcommission }}</td>
              </template>
            </v-data-table>
          </v-flex>
        </v-layout>

      </div>

      <div v-if="this.$login=='airline_staff'">

        <h2> View Top Booking Agents # of Sales Month </h2>
        <v-layout row wrap justify-center>
          <v-flex xs5 >
            <v-data-table :headers="headers_bookMonth" :items="items_bookMonth" hide-actions class="elevation-1">
              <template slot="items" slot-scope="props">
                <td class="text-xs-center">{{ props.item.booking_agent_id }}</td>
                <td class="text-xs-center">{{ props.item.numbertickets_month }}</td>

              </template>
            </v-data-table><br>
            <h2> View Top Booking Agents # of Sales Year </h2>
            <v-data-table :headers="headers_bookYear" :items="items_bookYear" hide-actions class="elevation-1">
              <template slot="items" slot-scope="props">
                <td class="text-xs-center">{{ props.item.booking_agent_id }}</td>
                <td class="text-xs-center">{{ props.item.numbertickets_year }}</td>

              </template>
            </v-data-table> <br>
            <h2> View Top Booking Agents Amount of Commission Year </h2>
            <v-data-table :headers="headers_bookComm" :items="items_bookComm" hide-actions class="elevation-1">
              <template slot="items" slot-scope="props">
                <td class="text-xs-center">{{ props.item.booking_agent_id }}</td>
                <td class="text-xs-center">{{ props.item.total_commission }}</td>

              </template>
            </v-data-table><br>
          </v-flex>
        </v-layout>


        <h2> View Top Customer Past Year: {{this.items_topCustomer.name}} ?</h2>
        <v-layout row wrap justify-center>
          <v-flex xs5 >
            <v-data-table :headers="headers_topCustomer" :items="items_topCustomer" hide-actions class="elevation-1">
              <template slot="items" slot-scope="props">
                <td class="text-xs-center">{{ props.item.flight_num }}</td>
              </template>
            </v-data-table>
          </v-flex>
        </v-layout>

        <br><br><h2> Total # Tickets Sold </h2>
        <h2> Past Month: {{this.item_ticketSold.month}} </h2>
        <h2> Past Year: {{this.item_ticketSold.year}} </h2>
        <v-btn flat color="primary" @click="dateChangeTicket">Change date range</v-btn>
          <div v-if="this.dateTicket==true">
            <v-form v-model="valid" ref="form2" lazy-validation>
              <v-layout row wrap justify-center>
                <v-flex xs3 >
                  <v-menu ref="menu3" lazy :close-on-content-click="false" v-model="menu3" transition="scale-transition" offset-y
                    full-width :nudge-right="40" min-width="290px" :return-value.sync="date3">
                    <v-text-field slot="activator" label="Start Date" v-model="date3" readonly></v-text-field>
                    <v-date-picker v-model="date3" no-title scrollable>
                      <v-spacer></v-spacer>
                      <v-btn flat color="primary" @click="menu3 = false">Cancel</v-btn>
                      <v-btn flat color="primary" @click="$refs.menu3.save(date3)">OK</v-btn>
                    </v-date-picker>
                  </v-menu>
                  <v-menu ref="menu4" lazy :close-on-content-click="false" v-model="menu4" transition="scale-transition" offset-y
                    full-width :nudge-right="40" min-width="290px" :return-value.sync="date4">
                    <v-text-field slot="activator" label="End Date" v-model="date4" readonly></v-text-field>
                    <v-date-picker v-model="date4" no-title scrollable>
                      <v-spacer></v-spacer>
                      <v-btn flat color="primary" @click="menu4 = false">Cancel</v-btn>
                      <v-btn flat color="primary" @click="$refs.menu4.save(date4)">OK</v-btn>
                    </v-date-picker>
                  </v-menu>
                  <v-btn @click="submit" :disabled="!valid">submit</v-btn>
                  <v-btn @click="clear">clear</v-btn>
                <br><br>
                </v-flex>
              </v-layout>
          </v-form>
        </div>
        <div v-if="this.showRange==true">
          <h2> # of tickets sold between {{this.date3}} and {{this.date4}}: {{this.items_ticketSold.range}}</h2>
        </div>

        <br><br><div>
          <v-layout row wrap justify-center>
            <v-flex xs5 >
              <h2> Top 3 Popular Destinations</h2>
              <v-data-table :headers="headers_destinations" :items="items_destinations" hide-actions class="elevation-1">
                <template slot="items" slot-scope="props">
                  <td class="text-xs-center">{{ props.item.destinations.three }}</td>
                  <td class="text-xs-center">{{ props.item.destinations.year }}</td>
                </template>
              </v-data-table><br>
            </v-flex>
          </v-layout>
        </div>

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
      dateRange:false,
      valid: true,
      menu1:false,
      date1:null, //start date of view commission
      menu2:false,
      date2:null, //end date of view commision
      headers_commission: [
        { text: 'Total Amount', value: 'totalamount' },
        { text: 'Average per Ticket', value: 'average' },
        { text: 'Total Number Sold', value: 'totalnumber' }
      ],
      items_commission: [],
      headers_customers: [
        { text: 'Customer', value: 'customer_email', sortable: false },
        { text: 'Number of Tickets', value: 'numbertickets' },
        { text: 'Amount of Commision', value: 'amountcommission' },
      ],
      items_customers: [],
      headers_bookMonth: [
        { text: 'Booking Agent ID', value: 'booking_agent_id', sortable: false },
        { text: '# of Tickets Sold', value: 'numbertickets_month', sortable: false },

      ],
      items_bookMonth: [],
      headers_bookYear: [
        { text: 'Booking Agent ID', value: 'booking_agent_id', sortable: false },
        { text: '# of Tickets Sold', value: 'numbertickets_year', sortable: false },
      ],
      items_bookYear: [],
      headers_bookComm: [
        { text: 'Booking Agent ID', value: 'booking_agent_id', sortable: false },
        { text: 'Amount of Commission', value: 'total_commission', sortable: false },

      ],
      items_bookComm: [],
      headers_topCustomer: [
        { text: 'Flight Number', value: 'flight_num', sortable: false },
      ],
      items_topCustomer: [],
      item_ticketSold: [],
      dateTicket: false,
      showRange: false,//show # tickets sold based on range
      menu3:false,
      date3:null, //start date of # tickets sold
      menu4:false,
      date4:null, //end date of # tickets sold
      headers_destinations: [
        { text: 'Top Destinations 3 Months', value: 'destination_three', sortable: false },
        { text: 'Top Destinations Year', value: 'destination_year', sortable: false },
      ],
      items_destinations: [],
      today: null,
      onemonth: null,
      sixmonths: null,
      threemonths: null,
      year: null,

    }
  },
  created () {
    // this.loginType()
    // this.$login = 'booking_agent'

    this.$login = 'airline_staff'
    this.getDate()
    console.log("this.$login", this.$login);
    if (this.$login == 'booking_agent'){
      this.getCommission()
      this.getTopCustomersBooking()
    }
    if (this.$login == 'airline_staff') {
      this.getTopBooking()
      this.getTopCustomerAirline()

    }
  },
  methods: {
    addMonths(date, months) {
      date.setMonth(date.getMonth() + months);
      return date;
    },
    getDate() {
      this.today = new Date()
      this.today = this.today.toISOString().substring(0, 10); //yyyy-mm-dd
      this.onemonth = this.addMonths(new Date(),-1).toISOString().substring(0, 10)
      this.sixmonths = this.addMonths(new Date(),-6).toISOString().substring(0, 10)
      this.threemonths = this.addMonths(new Date(),-3).toISOString().substring(0, 10)
      this.year = this.addMonths(new Date(),-12).toISOString().substring(0, 10)
      console.log("six, three, year", this.sixmonths, this.threemonths, this.year);
    },
    dateChangeTicket(){
      this.dateTicket = true
    },
    getTopCustomerAirline() { //top customers for airline staff
      const path = `http://localhost:5000/api/##` //commission
      var d = {
        "today": this.today,
        "year": this.year,
      }
      axios.post(path, d)
        .then(response => {
          var res = response.data //return flights
          console.log(res);
          //this.items_topCustomer = res
          //only give flight_num for that customer
        })
        .catch(error => {
          console.log("error => ", error);
        })
    },
    getTopBooking() { //top booking agents for airline staff
      const path = `http://localhost:5000/api/##` //commission
      var d = {
        "today": this.today,
        "onemonth": this.onemonth,
        "year": this.year,
      }
      axios.post(path, d)
        .then(response => {
          var res = response.data //return flights
          console.log(res);
          //this.items_bookMonth = res.bookMonth
          //this.items_bookYear = res.bookYear
          //this.items_bookComm = res.bookComm
        })
        .catch(error => {
          console.log("error => ", error);
        })
    },
    getTopCustomersBooking() { //top customers for booking agents
      const path = `http://localhost:5000/api/##` //commission
      var d = {
        "today": this.today,
        "sixmonths": this.sixmonths,
        "year": this.year,
      }
      axios.post(path, d)
        .then(response => {
          var res = response.data //return flights
          console.log(res);
          //this.items_customers = res.dataitems
        })
        .catch(error => {
          console.log("error => ", error);
        })
    },
    getCommission() {
      const path = `http://localhost:5000/api/##` //commission
      var d = {
        "today": this.today,
        "onemonth": this.onemonth,
      }
      axios.post(path, d)
        .then(response => {
          var res = response.data //return flights
          console.log(res);
          //this.items_commission = res.dataitems
        })
        .catch(error => {
          console.log("error =>", error);
        })
    },
    dateChange() {
      this.dateRange = true
    },
    clear() {
      this.$refs.form1.reset()
      this.$refs.form2.reset()

    },
    submit (){
      if (this.$refs.form1.validate()) { //search flights for staff
        const path = `http://localhost:5000/api/##` //commission
        var d = {
          "start_date": this.date1,
          "end_date": this.date2,
        }
        axios.post(path, d)
          .then(response => {
            var res = response.data //return flights
            console.log(res);
            //this.items_commission = res.dataitems
            this.dateRange = false //close the date range chooser
          })
          .catch(error => {
            console.log("error getting flights");
          })
      }
      if (this.$refs.form2.validate()) { //# tickets based on date range
        const path = `http://localhost:5000/api/##` //commission
        var d = {
          "start_date": this.date3,
          "end_date": this.date4,
        }
        axios.post(path, d)
          .then(response => {
            var res = response.data //return flights
            console.log(res);
            //this.items_ticketSold = res.dataitems
            this.dateTicket = false //close the date range chooser
            this.showRange = true //show # tickets sold based on range
          })
          .catch(error => {
            console.log("error getting flights");
          })
      }
    },
    loginType() {
      const path = `http://localhost:5000/api/####`
      var d = {
        "login_type": this.$login,
        "page_type": "statistics"
      }
      axios.post(path, d)
        .then(response => {
          var res = response.data //give me login_usertype,
          console.log(res);
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
    }
  }
}
</script>

<style scoped>

</style>
