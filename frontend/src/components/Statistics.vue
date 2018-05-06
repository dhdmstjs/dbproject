<template>
  <div>
    <v-app> <br><br>
      <div v-if="this.$login=='booking_agent'">

          <h2>Commission Data Default: Past 30 days</h2> <v-btn flat color="primary" @click="dateChange">Change date range</v-btn>

            <v-layout row wrap justify-center>
              <v-flex xs8 >
                  <h2>Total Amount</h2>
                    <span class="text-xs-center">{{ this.items_commission_total_cost }}</span>
                  <h2> Avg per Ticket </h2>
                    <span class="text-xs-center">{{ this.items_commission_avg_ticket_price }}</span>
                  <h2> Total Tickets Sold</h2>
                    <span class="text-xs-center">{{ this.items_commission_total_sold }}</span>
              </v-flex>
            </v-layout>
            <br><br><br>
        <!-- these dates are to choose date-->
          <div v-if="this.dateRange==true">
            <h2> Choose date range to specify commission data </h2>
            <v-layout row wrap justify-center>
              <v-flex xs3 >
                <v-form v-model="valid" ref="form1" lazy-validation>
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
                  <v-btn @click="submitComm" :disabled="!valid">submit</v-btn>
                  <v-btn @click="clear">clear</v-btn>
                  <br><br>
                </v-form>

              </v-flex>
            </v-layout>
        </div>

        <h2> View Top Customers # tickets past 6 months</h2>
        <v-layout row wrap justify-center>
          <v-flex xs5 >
            <v-data-table :headers="headers_customers_tickets" :items="items_customers_tickets" hide-actions class="elevation-1">
              <template slot="items" slot-scope="props">
                <td class="text-xs-left">{{ props.item.customer_email }}</td>
                <td class="text-xs-left">{{ props.item.count_t }}</td>
              </template>
            </v-data-table>
          </v-flex>
        </v-layout>

        <v-layout row wrap justify-center>
              <v-flex xs7 >
            <template>
            <bar-chart v-if="this.ticketDataFlag==true" :chartData="this.ticketData"
            :optionsData="this.ticketOptions"
            :width="400"
            :height="200"></bar-chart>
          </template>
        </v-flex>
        </v-layout>


        <br>
        <h2> View Top Customers Amount of Commission past year </h2>
        <v-layout row wrap justify-center>
          <v-flex xs5 >
            <v-data-table :headers="headers_customers_comm" :items="items_customers_comm" hide-actions class="elevation-1">
              <template slot="items" slot-scope="props">
                <td class="text-xs-left">{{ props.item.customer_email }}</td>
                <td class="text-xs-left">{{ props.item.sump }}</td>
              </template>
            </v-data-table>
          </v-flex>
        </v-layout>

        <v-layout row wrap justify-center>
              <v-flex xs7 >
            <template>
            <bar-chart v-if="this.commDataFlag==true" :chartData="this.commData"
            :optionsData="this.commOptions"
            :width="400"
            :height="200"></bar-chart>
          </template>
        </v-flex>
        </v-layout>

      </div>

      <div v-if="this.$login=='airline_staff'">

        <h2> View Top Booking Agents # of Sales Month </h2>
        <v-layout row wrap justify-center>
          <v-flex xs7 >
            <v-data-table :headers="headers_bookMonth" :items="items_bookMonth" hide-actions class="elevation-1">
              <template slot="items" slot-scope="props">
                <td class="text-xs-left">{{ props.item.email }}</td>
                <td class="text-xs-left">{{ props.item.tickets }}</td>
              </template>
            </v-data-table><br>
            <h2> View Top Booking Agents # of Sales Year </h2>
            <v-data-table :headers="headers_bookYear" :items="items_bookYear" hide-actions class="elevation-1">
              <template slot="items" slot-scope="props">
                <td class="text-xs-left">{{ props.item.email }}</td>
                <td class="text-xs-left">{{ props.item.tickets }}</td>

              </template>
            </v-data-table> <br>
            <h2> View Top Booking Agents Amount of Commission Year </h2>
            <v-data-table :headers="headers_bookComm" :items="items_bookComm" hide-actions class="elevation-1">
              <template slot="items" slot-scope="props">
                <td class="text-xs-left">{{ props.item.email }}</td>
                <td class="text-xs-cenleftter">{{ props.item.commission }}</td>

              </template>
            </v-data-table><br>
          </v-flex>
        </v-layout>


        <h2> View Top Customer Past Year: {{this.topCustomer_email}}</h2>
        <v-layout row wrap justify-center>
          <v-flex xs9 >
            <v-data-table :headers="headers_topCustomer" :items="items_topCustomer" hide-actions class="elevation-1">
              <template slot="items" slot-scope="props">
                <td class="text-xs-center">{{ props.item.departure_airport }}</td>
                <td class="text-xs-center">{{ props.item.departure_time }}</td>
                <td class="text-xs-center">{{ props.item.arrival_airport }}</td>
                <td class="text-xs-center">{{ props.item.arrival_time }}</td>

              </template>
            </v-data-table>
          </v-flex>
        </v-layout>

        <br><br><h2> Total # Tickets Sold </h2>
        <h2> # of tickets sold between {{this.date3}} and {{this.date4}}: {{this.soldTotal}}</h2>
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
                  <v-btn @click="submitTwo" :disabled="!valid">submit</v-btn>
                  <v-btn @click="clear">clear</v-btn>
                <br><br>
                </v-flex>
              </v-layout>
          </v-form>

        <div v-if="this.submitBar==true">
          <v-layout row wrap justify-center>
                <v-flex xs7 >
              <template>
              <bar-chart v-if="this.showData==true" :chartData="this.dataset"
              :optionsData="this.dataoptions"
              :width="400"
              :height="200"></bar-chart>
            </template>
          </v-flex>
        </v-layout>
        </div>

        <br><br><div>
          <v-layout row wrap justify-center>
            <v-flex xs7 >
              <h2> Top 3 Popular Destinations Months</h2>
              <v-data-table :headers="headers_dest_Month" :items="items_dest_Month" hide-actions class="elevation-1">
                <template slot="items" slot-scope="props">
                  <td class="text-xs-center">{{ props.item.airport_city }}</td>
                </template>
              </v-data-table><br>
              <h2> Top 3 Popular Destinations Year</h2>
              <v-data-table :headers="headers_dest_Year" :items="items_dest_Year" hide-actions class="elevation-1">
                <template slot="items" slot-scope="props">
                  <td class="text-xs-center">{{ props.item.airport_city }}</td>
                </template>
              </v-data-table><br>
            </v-flex>
          </v-layout>
        </div>

        <!-- pie chart -->
        <v-layout row wrap justify-center>
          <v-flex xs7 >
            <template>
            <pie-chart v-if="this.pieData==true" :chartData="this.dataPie"
            :optionsData="this.pieOptions"
            :width="400"
            :height="200"></pie-chart>
          </template>
        </v-flex>
        </v-layout>
        <br><br><br>
        <v-layout row wrap justify-center>
          <v-flex xs7 >
            <template>
            <pie-chart v-if="this.pieDataTwo==true" :chartData="this.dataPieTwo"
            :optionsData="this.pieOptionsTwo"
            :width="400"
            :height="200"></pie-chart>
          </template>
        </v-flex>
        </v-layout>


    </div>


  </v-app>
  </div>
</template>

<script>
import axios from 'axios'
import 'vuetify/dist/vuetify.min.css'
import BarChart from './Bar'
import PieChart from './Pie'
import Vue from 'vue'


export default {
  components: {
     'bar-chart': BarChart,
     'pie-chart': PieChart,

  },
  // extends: Bar
  data () {
    return {
      dateRange:false,
      valid: true,
      menu1:false,
      date1:null, //start date of view commission
      menu2:false,
      date2:null, //end date of view commision
      items_commission_total_cost: null,
      items_commission_avg_ticket_price: null,
      items_commission_total_sold: null,
      headers_customers_tickets: [
        { text: 'Customer', value: 'customer_email', sortable: false },
        { text: 'Number of Tickets', value: 'count_t', sortable:false },
      ],
      items_customers_tickets: [],
      headers_customers_comm: [
        { text: 'Customer', value: 'customer_email', sortable: false },
        { text: 'Amount of Commision', value: 'sump',sortable:false },
      ],
      items_customers_comm: [],
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
        { text: 'Departure Airport', value: 'departure_airport', sortable: false },
        { text: 'Departure Time', value: 'departure_time', sortable: false },
        { text: 'Arrival Airport', value: 'arrival_airport', sortable: false },
        { text: 'Arrival Time', value: 'arrival_time', sortable: false },

      ],
      items_topCustomer: [],
      topCustomer_email: null,
      item_ticketSold: [], //total number of tickets sold
      dateTicket: false,
      showRange: false,//show # tickets sold based on range
      menu3:false,
      date3:null, //start date of # tickets sold
      menu4:false,
      date4:null, //end date of # tickets sold
      headers_dest_Month: [
        { text: 'Top Destinations 3 Months', value: 'destination_three', sortable: false },
      ],
      items_dest_Month: [],
      headers_dest_Year: [
        { text: 'Top Destinations Year', value: 'destination_year', sortable: false },
      ],
      items_dest_Year: [],
      today: null,
      onemonth: null,
      sixmonths: null,
      threemonths: null,
      year: null,
      soldTotal: null, //value for view reports between dates
      labels: [],
      dataset: {
        labels: [],
        datasets: [{
          label: '',
          data: null,
          backgroundColor: '#f87979'
        }]
      },
      dataoptions: {
        title: {
          display: true,
          text: '',
        },
        scales: {
          yAxes: [{id: 'y-axis-1', ticks: {min: 0}}]
        }
      },
      dataPie: {
        labels: [],
        datasets: [{
          label: '',
          data: null,
          backgroundColor: [

            '#00D8FF',
            '#DD1B16'
          ],
        }]
      },
      pieOptions: {
        title: {
          display: true,
          text: '',
        }
      },
      dataPieTwo: {
        labels: [],
        datasets: [{
          backgroundColor: [
            '#41B883',
            '#E46651',

          ],
          label: '',
          data: null,
        }]
      },
      pieOptionsTwo: {
        title: {
          display: true,
          text: '',
        }
      },
      pieDataTwo: false,
      pieData: false, //for piechart
      submitBar: false, //toggle barchart
      showData: false, //toggle dat sent to barchart
      ticketDataFlag: false, //for bar for BA
      commDataFlag: false, //for bar for BA
      ticketData: { //# tickets
        labels: [],
        datasets: [{
          label: '',
          data: null,
          backgroundColor: '#f87979'

        }]
      },
      ticketOptions: {
        title: {
          display: true,
          text: '',
        },
        scales: {
          yAxes: [{id: 'y-axis-1', ticks: {min: 0}}]
        }
      },
      commData: { ///amount of commission
        labels: [],
        datasets: [{
          label: '',
          data: null,
          backgroundColor: '#f87979'

        }]
      },
      commOptions: {
        title: {
          display: true,
          text: '',
        },
        scales: {
          yAxes: [{id: 'y-axis-1', ticks: {min: 0}}]
        }
      },
    }
  },
  created () {
    this.getDate()

    const path = `http://localhost:5000/session/vars`;
    axios.post(path)
      .then(response => {
        let res = response.data;
        console.log("res" ,res);
        Vue.prototype.$login = '' //set user type here
        console.log("this.$login", this.$login);
        if (this.$login == 'booking_agent'){
          console.log("hi");
          this.getCommission()
          this.getTopCustomersBooking()
        }
        if (this.$login == 'airline_staff') {
          this.getTopBooking()
          this.getTopCustomerAirline()
          this.getData()
          this.getPie()
        }
      })
      .catch(error => {
        console.log('getting session vars-->', error);
      });

  },
  methods: {
    getData() {
      if (this.$login == 'airline_staff') {
        const path1 = `http://localhost:5000/api/bookingagenttopdestinations`
        axios.get(path1)
          .then(response => {
            var res = response.data
            console.log("res top dest", res);
            this.items_dest_Month = res.month_destinations
            this.items_dest_Year = res.year_destinations
          })
          .catch(error => {
            console.log("error => ", error);
          })
        }

    if (this.$login == 'booking_agent') {

      const path2 = `http://localhost:5000/api/bookingagentcommission`
      d2 = {
        'date1': this.today,
        'date2': this.month, //30 days ago
        'username': 'colton@nyu'
      }
      axios.post(path2, d2)
        .then(response => {
          var res = response.date
          console.log("reshellooo", res);
          // this.items_commission = res
        })
        .catch(error => {
          console.log("error => ", error);
        })


      }

    },
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
      const path = `http://localhost:5000/api/viewfrequentcustomers`
      var d = {
        "date2": this.today,
        "date1": this.year,
        "username": 'colton@nyu'
      }
      axios.post(path, d)
        .then(response => {
          var res = response.data //return flights
          console.log(res);
          this.topCustomer_email = res.customers[0].email
          this.items_topCustomer = res.customers[0].flights
          // only give flight_num for that customer
        })
        .catch(error => {
          console.log("error => ", error);
        })
    },
    getTopBooking() { //top booking agents for airline staff
      const path = `http://localhost:5000/api/airlinestaffbookingagents` //commission
      axios.get(path)
        .then(response => {
          var res = response.data //return flights
          console.log(res);
          this.items_bookMonth = res.ticket_month_data
          this.items_bookYear = res.ticket_year_data
          this.items_bookComm = res.commission_year_data
        })
        .catch(error => {
          console.log("error => ", error);
        })
    },
    getTopCustomersBooking() { //top customers for booking agents
      const path = `http://localhost:5000/api/bookingagenttopcustomers` //commission
      var d = {
        "date2": this.today,
        "date1": this.sixmonths,
        'username': 'c'
      }
      console.log("d",d);
      axios.post(path, d)
        .then(response => {
          var res = response.data //return flights
          console.log("top cust",res);
          this.items_customers_tickets = res.ticket_data
          this.items_customers_comm = res.commission_data
          this.ticketDataFlag = true
          this.commDataFlag = true
          this.ticketData.labels = res.ticket_customers.labels
          this.ticketData.datasets.data = res.ticket_customers.values
          this.ticketData.datasets[0].label ="hello"
          this.ticketData.datasets[0].data = res.ticket_customers.values
          this.ticketOptions.title.text = 'Top Customers # of tickets'

          this.commData.labels = res.commission_customers.labels
          this.commData.datasets.data = res.commission_customers.values
          this.commData.datasets[0].label ="hello"
          this.commData.datasets[0].data = res.commission_customers.values
          this.commOptions.title.text = 'Top Customers Commission'
        })
        .catch(error => {
          console.log("error => ", error);
        })



    },
    getCommission() {
      const path = `http://localhost:5000/api/bookingagentcommission` //commission
      console.log("thismonth", this.onemonth);
      console.log("today", this.today);
      var d = {
        "date2": this.today,
        "date1": this.onemonth,
        "username": 'c',
      }
      axios.post(path, d)
        .then(response => {
          var res = response.data //return flights
          console.log("res",res);
          this.items_commission_total_cost= res.total_cost
          this.items_commission_avg_ticket_price = res.avg_ticket_price
          this.items_commission_total_sold = res.total_sold
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
    submitComm (){
      const path = `http://localhost:5000/api/bookingagentcommission` //commission
      var d = {
        "date1": this.date1,
        "date2": this.date2,
        "username": 'c'
      }
      axios.post(path, d)
        .then(response => {
          var res = response.data //return flights
          console.log(res);
          this.items_commission_total_cost= res.total_cost
          this.items_commission_avg_ticket_price = res.avg_ticket_price
          this.items_commission_total_sold = res.total_sold
          this.dateRange = false //close the date range chooser
        })
        .catch(error => {
          console.log("error getting flights");
        })

    },
    submitTwo( ){
      const path4 = `http://localhost:5000/api/viewreports`
        var d2 = {
          "date2": this.date4,
          "date1": this.date3,
        }
        axios.post(path4, d2)
          .then(response => {
            var res = response.data
            this.soldTotal = res.total
            console.log("res view reports", res);
            this.submitBar = true

            this.renderBar(res)


          })
          .catch(error => {
            console.log("error => ", error);
          })

    },
    renderBar(items) {
      console.log("items",items);
      this.showData = true

      this.dataset.labels = items.labels
      this.dataset.datasets.data = items.values
      this.dataset.datasets[0].label = "tickets"
      this.dataset.datasets[0].data = items.values
      this.dataoptions.title.text = 'total # tickets sold /month'
      console.log("render labels", this.dataset.labels)
      console.log("this. data testing", this.dataset.datasets.data);
    },

    getPie() {
      const path = `http://localhost:5000/api/comparerevenue`
        axios.get(path)
          .then(response => {
            var res = response.data
            console.log("res view compare", res);
            this.pieData = true
            let month_labels = []
            let year_labels = []
            month_labels.push('direct_sales_month')
            year_labels.push('direct_sales_year')
            month_labels.push('indirect_sales_month')
            year_labels.push('indirect_sales_year')
            let month_values = [res.direct_sales_month, res.agents_sales_month]
            console.log(month_values)
            let year_values = [res.direct_sales_year, res.agent_sales_year]

            this.dataPie.labels = month_labels
            this.dataPie.datasets.data = month_values
            this.dataPie.datasets[0].data = month_values
            this.pieOptions.title.text = 'Month Sales'

            this.pieDataTwo = true
            this.dataPieTwo.labels = year_labels
            this.dataPieTwo.datasets.data = year_values
            this.dataPieTwo.datasets[0].data = year_values
            this.pieOptionsTwo.title.text = 'Year Sales'




          })
          .catch(error => {
            console.log("error => ", error);
          })
    }
    // loginType() {
    //   const path = `http://localhost:5000/api/####`
    //   var d = {
    //     "login_type": this.$login,
    //     "page_type": "statistics"
    //   }
    //   axios.post(path, d)
    //     .then(response => {
    //       var res = response.data //give me login_usertype,
    //       console.log(res);
    //       if (res.login_usertype == 'booking_agent') {
    //         //this.items_booking = res.dataitems
    //       }
    //       if (res.login_usertype == 'airline_staff') {
    //         //this.items_airline = res.dataitems
    //       }
    //     })
    //     .catch(error => {
    //       console.log("error changing status");
    //     })
    // }
  }
}
</script>

<style scoped>

</style>
