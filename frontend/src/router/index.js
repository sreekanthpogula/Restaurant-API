import Vue from 'vue'
import Router from 'vue-router'
import Orders from '../components/Orders.vue'
import Navbar from '../components/Navbar.vue'
import Home from '../components/Home.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Navbar',
      component: Navbar
    },
    {
      path: '/home',
      name: 'Home',
      component: Home
    },
    {
      path: '/orders',
      name: 'Orders',
      component: Orders
    },
    
  ]
})
