<template>
  <div>
    <v-app>
    <v-layout row wrap justify-center>
    <v-flex xs5 >
      <h1>Forms</h1><br>
      <v-expansion-panel>
        <v-expansion-panel-content>
          <div slot="header">Create new flight</div>
          <v-card>
            <v-form v-model="valid" ref="form" lazy-validation>
                <v-text-field
                label="Depart From" v-model="depart" :rules="departRules" required></v-text-field>
                <v-text-field
                label="Arrive At" v-model="arrive" :rules="arriveRules" required></v-text-field>
              <v-btn @click="submit" :disabled="!valid">submit</v-btn>
              <v-btn @click="clear">clear</v-btn>
            </v-form>
          </v-card>
        </v-expansion-panel-content>

        <v-expansion-panel-content>
          <div slot="header">Change flight status</div>
          <v-card>
            <v-form v-model="valid" ref="form" lazy-validation>
                <v-text-field
                label="Depart From" v-model="depart" :rules="departRules" required></v-text-field>
                <v-text-field
                label="Arrive At" v-model="arrive" :rules="arriveRules" required></v-text-field>
              <v-btn @click="submit" :disabled="!valid">submit</v-btn>
              <v-btn @click="clear">clear</v-btn>
            </v-form>
          </v-card>
        </v-expansion-panel-content>

        <v-expansion-panel-content>
          <div slot="header">Add airplane to system</div>
          <v-card>
            <v-form v-model="valid" ref="form" lazy-validation>
                <v-text-field
                label="Depart From" v-model="depart" :rules="departRules" required></v-text-field>
                <v-text-field
                label="Arrive At" v-model="arrive" :rules="arriveRules" required></v-text-field>
              <v-btn @click="submit" :disabled="!valid">submit</v-btn>
              <v-btn @click="clear">clear</v-btn>
            </v-form>
          </v-card>
        </v-expansion-panel-content>

        <v-expansion-panel-content>
          <div slot="header">Add airport to system</div>
          <v-card>
            <v-form v-model="valid" ref="form" lazy-validation>
                <v-text-field
                label="Depart From" v-model="depart" :rules="departRules" required></v-text-field>
                <v-text-field
                label="Arrive At" v-model="arrive" :rules="arriveRules" required></v-text-field>
              <v-btn @click="submit" :disabled="!valid">submit</v-btn>
              <v-btn @click="clear">clear</v-btn>
            </v-form>
          </v-card>

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
      date: '',
      menu:false,
      valid: true,
      depart: '',
      departRules: [v => !!v || 'Depart City is required'],
      arrive: '',
      arriveRules: [v => !!v || 'Depart City is required'],
    }
  },
  created () {

  },
  methods: {
    submit () {
      if (this.$refs.form.validate()) {
        // Native form submission is not yet supported

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
  }
}
</script>

<style scoped>

</style>
