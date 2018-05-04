<template>
  <div>
    <v-app>
      <h1>Track Spending</h1><br>
      <h2> Total Amount spent past year: {{this.spending}} </h2>
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

      <h2> Bar Graph </h2>


  </v-app>
  </div>
</template>

<script>
import axios from 'axios'
import 'vuetify/dist/vuetify.min.css'

export default {
  data () {
    return {
      menu1: false,
      menu2: false,
      date1: '',
      date2: '',
      valid: true,
      spending: '',
      range: false,
      today: null,
      sixmonths: null,
      year: null,
    }
  },
  created () {
    //this.getData()
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
    },
    getData() {
      const path = `http://localhost:5000/api/customerspending` //commission
      var d = {
        "username" : "colton@nyu",
        "date1": this.today,
        "date2": this.sixmonths,
        "year": this.year,
      }
      axios.post(path,d)
        .then(response => {
          var res = response.data //return flights
          console.log(res);
          //this.spending = res.data???
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
          "date1": this.date1,
          "date2": this.date2,
        }
        axios.post(path, d)
          .then(response => {
            var res = response.data //return flights
            console.log(res);
            //this.spending = res.data???
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
