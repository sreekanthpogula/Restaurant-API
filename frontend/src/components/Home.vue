<template>
    <v-container>
      <v-card>
        <v-card-title>Welcome to the Restaurant</v-card-title>
        <v-card-text>
          You can now order your favorite food items.
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="goToOrders">Order Now</v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </template>
  <script>
  export default {
    methods: {
      goToOrders() {
        this.$router.push('/orders')
      }
    }
  }
  </script>
  