import Vue from 'vue'
import App from './App'
import router from './router'
import Vuetify from 'vuetify'
import VueSweetalert2 from 'vue-sweetalert2'
import VueCharts from 'vue-chartjs'
import 'vuetify/dist/vuetify.min.css'

Vue.config.productionTip = false
Vue.use(Vuetify)
Vue.use(VueSweetalert2)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
