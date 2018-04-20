<template>
  <div>
    <v-app>
    <!-- <p>Random number from backend: {{ randomNumber }}</p>
    <button @click="getRandom">New random number</button> -->

    <!-- Login/Register -->
    <v-layout row wrap justify-end>
      <v-flex xs4>
      <v-btn color="primary" dark @click.stop="login = true">Login</v-btn>
      <v-btn color="primary" dark @click.stop="register = true">Register</v-btn>
      <!-- Login Content -->
        <v-dialog v-model="login" max-width="500px">
            <v-card>
              <v-card-title>
                Login
              </v-card-title>
              <v-card-text>
                <v-form v-model="valid" ref="form" lazy-validation>
                    <v-text-field
                    label="Username" v-model="username" :rules="usernameRules" required></v-text-field>
                    <v-text-field
                    label="Password" v-model="password" :rules="passwordRules" required></v-text-field>
                  <v-btn @click="login" :disabled="!valid">Login</v-btn>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-btn color="primary" flat @click.stop="login=false">Close</v-btn>
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
                    <v-form v-model="valid" ref="form" lazy-validation>
                        <v-text-field
                        label="Username" v-model="username" :rules="usernameRules" required></v-text-field>
                        <v-text-field
                        label="Password" v-model="password" :rules="passwordRules" required></v-text-field>
                        <v-checkbox label="Airline Staff" v-model="checkbox1"></v-checkbox>
                        <v-checkbox label="Booking Agent" v-model="checkbox2"></v-checkbox>

                      <v-btn @click="register" :disabled="!valid">Register</v-btn>
                    </v-form>
                  </v-card-text>
                  <v-card-actions>
                    <v-btn color="primary" flat @click.stop="register=false">Close</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
        </v-flex>
      </v-layout>

    <!-- search box -->
    <br>
    <v-layout row wrap justify-center>
      <v-flex xs4>
        <h2> Search for Flights</h2>

        <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field
            label="Depart From" v-model="depart" :rules="departRules" required></v-text-field>
            <v-text-field
            label="Arrive At" v-model="arrive" :rules="arriveRules" required></v-text-field>
                <v-menu
                  ref="menu" lazy :close-on-content-click="false" v-model="menu" transition="scale-transition" offset-y
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

<!-- data table -->
  <br>
    <div>
      <v-data-table
        :headers="headers"
        :items="items"
        hide-actions
        class="elevation-1"
      >
        <template slot="items" slot-scope="props">
          <td>{{ props.item.name }}</td>
          <td class="text-xs-right">{{ props.item.calories }}</td>
          <td class="text-xs-right">{{ props.item.fat }}</td>
          <td class="text-xs-right">{{ props.item.carbs }}</td>
          <td class="text-xs-right">{{ props.item.protein }}</td>
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

    <v-card height="200px" flat>
      <v-bottom-nav absolute :value="true" :active.sync="e1" color="transparent">
        <v-btn flat color="teal" value="recent">
            <span>Login</span>
            <v-icon>Login</v-icon>
        </v-btn>
        <v-btn flat color="teal" value="favorites">
          <span>Favorites</span>
          <v-icon>favorite</v-icon>
        </v-btn>
        <v-btn flat color="teal" value="nearby">
          <span>Nearby</span>
          <v-icon>place</v-icon>
        </v-btn>
      </v-bottom-nav>
    </v-card>
  </v-app>
  </div>
</template>

<script>
import axios from 'axios'
import 'vuetify/dist/vuetify.min.css'

export default {
  data () {
    return {
      randomNumber: 0,
      e1: 'recent',
      date: null,
      menu: false,
      valid: true,
      depart: '',
      departRules: [v => !!v || 'Depart City is required'],
      arrive: '',
      arriveRules: [v => !!v || 'Depart City is required'],
      headers: [
      {
        text: 'Dessert (100g serving)',
        align: 'left',
        sortable: false,
        value: 'name'
      },
      { text: 'Calories', value: 'calories' },
      { text: 'Fat (g)', value: 'fat' },
      { text: 'Carbs (g)', value: 'carbs' },
      { text: 'Protein (g)', value: 'protein' },
      { text: 'Actions', value: 'name', sortable: false }
    ],
     items: [],
     menu: [
       {item:'Login/Register'},
       {item:'Other stuff'}
     ],
     login: false,
     register: false,
     checkbox1: false, //airline staff
     checkbox2: false, //booking agent
     username: '',
     usernameRules: [v => !!v || 'username is required'],
     password: '',
     passwordRules: [v => !!v || 'password is required'],
    }
  },
  created () {
    this.initialize()
  },
  methods: {
    submit () {
      if (this.$refs.form.validate()) {
        // Native form submission is not yet supported
        console.log("this.depart",this.depart);
        console.log("this.arrive",this.arrive);
        console.log("this.date",this.date);
        // axios.post('/api/submit', {
        //   name: this.name,
        //   email: this.email,
        //   select: this.select,
        //   checkbox: this.checkbox
        // })
      }
    },
    clear () {
      this.$refs.form.reset()
    },
    buyItem (item) {
      const index = this.items.indexOf(item)
      confirm('Are you sure you want to buy this item?') && this.items.splice(index, 1)
    },
    initialize () {
      this.items = [
        {
          name: 'Frozen Yogurt',
          calories: 159,
          fat: 6.0,
          carbs: 24,
          protein: 4.0
        },
        {
          name: 'Ice cream sandwich',
          calories: 237,
          fat: 9.0,
          carbs: 37,
          protein: 4.3
        },
        {
          name: 'Eclair',
          calories: 262,
          fat: 16.0,
          carbs: 23,
          protein: 6.0
        },
        {
          name: 'Cupcake',
          calories: 305,
          fat: 3.7,
          carbs: 67,
          protein: 4.3
        },
        {
          name: 'Gingerbread',
          calories: 356,
          fat: 16.0,
          carbs: 49,
          protein: 3.9
        }
      ]
    },
  }
}
</script>

<style scoped>


</style>
