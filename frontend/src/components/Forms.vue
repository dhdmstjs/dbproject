<template>
  <div>
    <v-app>
    <v-layout row wrap justify-center>
    <v-flex xs7 >
      <h1>Forms</h1><br>
      <v-expansion-panel>
        <v-expansion-panel-content>
          <div slot="header">Create new flight</div>
          <v-layout row wrap justify-center>
            <v-flex xs6 >
            <v-card>
              <v-form v-model="valid" ref="form1" lazy-validation>
                  <v-text-field
                  label="Airline Name" v-model="airline_name" required></v-text-field>
                  <v-text-field
                  label="Flight Number" v-model="flight_num" required></v-text-field>
                  <v-text-field
                  label="Departure Airport" v-model="departure_airport" required></v-text-field>
                  <v-menu ref="menu1" lazy :close-on-content-click="false" v-model="menu1" transition="scale-transition" offset-y
                    full-width :nudge-right="40" min-width="290px" :return-value.sync="date1">
                    <v-text-field slot="activator" label="Depart Date" v-model="date1" readonly></v-text-field>
                    <v-date-picker v-model="date1" no-title scrollable>
                      <v-spacer></v-spacer>
                      <v-btn flat color="primary" @click="menu1 = false">Cancel</v-btn>
                      <v-btn flat color="primary" @click="$refs.menu1.save(date1)">OK</v-btn>
                    </v-date-picker>
                  </v-menu>

                  <v-menu ref="menu2" lazy :close-on-content-click="false" v-model="menu2" transition="scale-transition" offset-y
                    full-width :nudge-right="40" min-width="290px" :return-value.sync="time1">
                    <v-text-field slot="activator" label="Depart Time" v-model="time1" prepend-icon="access_time" readonly></v-text-field>
                    <v-time-picker v-model="time1" @change="$refs.menu2.save(time1)"></v-time-picker>
                  </v-menu>

                  <v-text-field
                  label="Arrival Airport" v-model="arrival_airport" required></v-text-field>

                  <v-menu ref="menu3" lazy :close-on-content-click="false" v-model="menu3" transition="scale-transition" offset-y
                    full-width :nudge-right="40" min-width="290px" :return-value.sync="date2">
                    <v-text-field slot="activator" label="Arrival Date" v-model="date2" readonly></v-text-field>
                    <v-date-picker v-model="date2" no-title scrollable>
                      <v-spacer></v-spacer>
                      <v-btn flat color="primary" @click="menu3 = false">Cancel</v-btn>
                      <v-btn flat color="primary" @click="$refs.menu3.save(date2)">OK</v-btn>
                    </v-date-picker>
                  </v-menu>

                  <v-menu ref="menu4" lazy :close-on-content-click="false" v-model="menu4" transition="scale-transition" offset-y
                    full-width :nudge-right="40" min-width="290px" :return-value.sync="time2">
                    <v-text-field slot="activator" label="Arrival Time" v-model="time2" prepend-icon="access_time" readonly></v-text-field>
                    <v-time-picker v-model="time2" @change="$refs.menu4.save(time2)"></v-time-picker>
                  </v-menu>


                  <v-text-field
                  label="Price" v-model="price" required></v-text-field>
                  <v-text-field
                  label="Status" v-model="flight_status" required></v-text-field>
                  <v-text-field
                  label="Airplane Id" v-model="airplane_id" required></v-text-field>
                <v-btn @click="submit1" :disabled="!valid">submit</v-btn>
                <v-btn @click="clear">clear</v-btn>
              </v-form>
            </v-card>
          </v-flex>
        </v-layout>

        </v-expansion-panel-content>

        <v-expansion-panel-content>
          <div slot="header">Change flight status</div>
          <v-layout row wrap justify-center>
            <v-flex xs6 >
          <v-card>
            <v-form v-model="valid" ref="form2" lazy-validation>
                <v-text-field
                label="Airline Name" v-model="airline_name" required></v-text-field>
                <v-text-field
                label="Flight Number" v-model="flight_num" required></v-text-field>
                <v-text-field
                label="Status" v-model="flight_status" required></v-text-field>
              <v-btn @click="submit2" :disabled="!valid">submit</v-btn>
              <v-btn @click="clear">clear</v-btn>
            </v-form>
          </v-card>
        </v-flex>
      </v-layout>
        </v-expansion-panel-content>

        <v-expansion-panel-content>
          <div slot="header">Add airplane to system</div>
          <v-layout row wrap justify-center>
            <v-flex xs6 >
          <v-card>
            <v-form v-model="valid" ref="form3" lazy-validation>
                <v-text-field
                label="Airline Name" v-model="airline_name" required></v-text-field>
                <v-text-field
                label="Airplane ID" v-model="airplane_id" required></v-text-field>
                <v-text-field
                label="Seats" v-model="seats" required></v-text-field>
              <v-btn @click="submit3" :disabled="!valid">submit</v-btn>
              <v-btn @click="clear">clear</v-btn>
            </v-form>
          </v-card>
        </v-flex>
      </v-layout>
        </v-expansion-panel-content>

        <v-expansion-panel-content>
          <div slot="header">Add airport to system</div>
          <v-layout row wrap justify-center>
            <v-flex xs6 >
          <v-card>
            <v-form v-model="valid" ref="form4" lazy-validation>
                <v-text-field
                label="Airport Name" v-model="airport_name" required></v-text-field>
                <v-text-field
                label="Airport City" v-model="airport_city" required></v-text-field>
              <v-btn @click="submit4" :disabled="!valid">submit</v-btn>
              <v-btn @click="clear">clear</v-btn>
            </v-form>
          </v-card>
        </v-flex>
        </v-layout>
        </v-expansion-panel-content>
    </v-expansion-panel>

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
      menu1: false, //dept day form1
      date1: null,
      menu2: false, //dept time form1
      time1: null,
      menu3: false, //arrival day form1
      date2: null,
      menu4: false, //arrival time form1
      time2: null,
      valid: true,
      airline_name: '',
      flight_num: '',
      departure_airport: '',
      arrival_airport: '',
      price: '',
      flight_status: '',
      airplane_id: '',
      airport_name: '',
      airport_city: '',
      seats: '',
      depart: '',
      departRules: [v => !!v || 'Depart City is required'],
      arrive: '',
      arriveRules: [v => !!v || 'Depart City is required'],
    }
  },

  methods: {
    submit1(item) {
      console.log("item", item);
      if (this.$refs.form1.validate()) {
        console.log(
          this.airline_name,
          this.flight_num,
          this.departure_airport,
          this.date1,
          this.time1,
          this.date2,
          this.time2,
          this.arrival_airport,
          this.price,
          this.flight_status,
          this.airplane_id
        );
        const path = `http://localhost:5000/api/createflight`;
        var d = {"airline_name":this.airline_name, "flight_num":this.flight_num, "departure_airport":this.departure_airport, "date1":this.date1, "time1":this.time1, "date2":this.date2, "time2":this.time2, "arrival_airport":this.arrival_airport, "price":this.price, "flight_status":this.flight_status, "airplane_id":this.airplane_id};
        console.log(d);
        axios.post(path,d)
          .then(response => {
            var res = response.data;
            console.log(res['success']);
            console.log(res['message']);
          })
          .catch(error => {
            console.log('getting flights -->', error);
          });
      }
    },
    submit2(item) {
      if (this.$refs.form2.validate()) {
        console.log(
          this.airline_name,
          this.flight_num,
          this.flight_status,
        );
      }
    },
    submit3(item) {
      if (this.$refs.form3.validate()) {
        console.log(
          this.airline_name,
          this.airplane_id,
          this.seats,
        );
      }
    },
    submit4(item) {
      if (this.$refs.form4.validate()) {
        console.log(
          this.airport_name,
          this.airport_city,
        );
      }
    },
    clear () {
      this.$refs.form1.reset()
    },
  }
}
</script>

<style scoped>

</style>
