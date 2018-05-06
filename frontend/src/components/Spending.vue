<template>
  <div>
    <v-app>
      <h1>Track Spending</h1><br>
      <h2> Total Amount spent past year: {{this.spending_year}} </h2>

      <v-btn flat color="primary" @click="dateRange">Change date range</v-btn>
        <div v-if="this.range==true">
          <v-form v-model="valid" ref="form" lazy-validation>
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
      <h2> Total Amount spent on range: {{this.spending_range}} </h2>
      <v-layout row wrap justify-center>
            <v-flex xs7 >
          <template>
          <bar-chart v-if="this.chartFlag==true" :chartData="this.spendingData"
          :optionsData="this.spendingOptions"
          :width="400"
          :height="200"></bar-chart>
        </template>
      </v-flex>
      </v-layout>

      <!-- bar chart for when range set -->
      <v-layout row wrap justify-center>
            <v-flex xs7 >
          <template>
          <bar-chart v-if="this.chartFlag2==true" :chartData="this.spendingDataTwo"
          :optionsData="this.spendingOptionsTwo"
          :width="400"
          :height="200"></bar-chart>
        </template>
      </v-flex>
      </v-layout>



  </v-app>
  </div>
</template>

<script>
import axios from 'axios'
import 'vuetify/dist/vuetify.min.css'
import BarChart from './Bar'
import Vue from 'vue'

export default {
  components: {
    'bar-chart': BarChart,

  },
  data () {
    return {
      menu1: false,
      menu2: false,
      date1: '',
      date2: '',
      valid: true,
      spending_year: '',
      range: false,
      today: null,
      sixmonths: null,
      year: null,
      spendingData: { //# tickets
        labels: [],
        datasets: [{
          label: '',
          data: null,
          backgroundColor: '#f87979'

        }]
      },
      spendingOptions: {
        title: {
          display: true,
          text: '',
        },
        scales: {
          yAxes: [{id: 'y-axis-1', ticks: {min: 0}}]
        }
      },
      chartFlag: false,
      spendingDataTwo: { //second bar chart
        labels: [],
        datasets: [{
          label: '',
          data: null,
          backgroundColor: '#f87979'

        }]
      },
      spendingOptionsTwo: {
        title: {
          display: true,
          text: '',
        },
        scales: {
          yAxes: [{id: 'y-axis-1', ticks: {min: 0}}]
        }
      },
      chartFlag2: false,
      username: null,
    }
  },
  created () {
    const path = `http://localhost:5000/session/vars`;
    axios.post(path)
      .then(response => {
        let res = response.data;
        console.log("res" ,res);
        Vue.prototype.$login = res.role //set user type here
        this.username = res.username
      })
      .catch(error => {
        console.log('getting session vars-->', error);
      });
    this.getDate()
  },
  methods: {
    addMonths(date, months) {
      date.setMonth(date.getMonth() + months);
      return date;
    },
    getDate() {
      this.today = new Date()
      this.today = this.today.toISOString().substring(0, 10); //yyyy-mm-dd
      this.sixmonths = this.addMonths(new Date(),-6).toISOString().substring(0, 10)
      this.year = this.addMonths(new Date(),-12).toISOString().substring(0, 10)
      this.getData()
    },
    getData() {
      const path = `http://localhost:5000/api/customerspending` //commission
      var d = {
        "username" : this.username,
        "date2": this.today,
        "date1": this.sixmonths,
      }
      console.log("d",d);
      axios.post(path,d)
        .then(response => {
          var res = response.data //return flights
          console.log("test",res);
          // this.spending = res.total
          this.chartFlag = true
          this.spending_range = res.total
          this.spendingData.labels = res.labels
          this.spendingData.datasets.data = res.vals
          this.spendingData.datasets[0].label = "tickets"
          this.spendingData.datasets[0].data = res.vals
          this.spendingOptions.title.text = 'total $$ spent past 6 months'
        })
        .catch(error => {
          console.log("error => ", error);
        })

        var d2 = {
          "username" : this.username,
          "date2": this.today,
          "date1": this.year,
        }
        axios.post(path,d2)
          .then(response => {
            var res = response.data //return flights
            console.log("test",res);
            this.spending_year = res.total
          })
          .catch(error => {
            console.log("error => ", error);
          })
    },
    dateRange () {
      this.range = true
    },
    submit () {
      if (this.$refs.form.validate()) {
        const path = `http://localhost:5000/api/customerspending` //commission
        var d = {
          "username" : this.username,
          "date1": this.date1,
          "date2": this.date2,
          "year": this.year,
        }
        axios.post(path, d)
          .then(response => {
            var res = response.data //return flights
            console.log("testdata",res);
            this.spending = res.total
            this.chartFlag = false
            this.chartFlag2 = true
            this.spendingDataTwo.labels = res.labels
            this.spendingDataTwo.datasets.data = res.vals
            this.spendingDataTwo.datasets[0].label = "tickets"
            this.spendingDataTwo.datasets[0].data = res.vals
            this.spendingOptionsTwo.title.text = 'total $$ spent'
          })
          .catch(error => {
            console.log("error => ", error);
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
