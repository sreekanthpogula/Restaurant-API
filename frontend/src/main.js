import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import axios from 'axios'
import store from './store'

Vue.config.productionTip = false

const axiosInstance = axios.create({
  baseURL: 'http://localhost:5000', // replace with your API endpoint
});

Vue.prototype.$http = axiosInstance

new Vue({
  router,
  vuetify,
  store,
  render: h => h(App)
}).$mount('#app')
