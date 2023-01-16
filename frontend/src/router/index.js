import Vue from 'vue'
import Router from 'vue-router'
import Orders from '../components/Orders.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Orders',
      component: Orders
    }
  ]
})
