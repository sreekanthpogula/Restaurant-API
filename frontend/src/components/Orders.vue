<template>
    <v-container>
      <v-row>
        <v-col v-for="order in orders" :key="order.order_id" cols="12" sm="6" md="4">
          <v-card>
            <v-card-title>Order ID: {{ order.order_id }}</v-card-title>
            <v-card-subtitle>Customer ID: {{ order.customer_id }}</v-card-subtitle>
            <v-card-text>
              <p>Status: {{ order.status }}</p>
              <p>Order Time: {{ order.order_time }}</p>
              <p>Items:</p>
              <ul>
                <li v-for="order in orders" :key="order.order_id">{{ item.Item_name }} - Quantity: {{ item.Quantity }} - Size: {{ item.size }}</li>
              </ul>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        orders: []
      }
    },
    methods: {
      fetchOrders() {
        axios.get('/orders')
          .then(response => {
            this.orders = response.data;
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    mounted() {
      this.fetchOrders();
    }
  }
  </script>
  