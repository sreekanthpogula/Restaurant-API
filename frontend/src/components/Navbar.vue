<template>
  <v-app-bar>
    <v-toolbar-title class="ml-0">
      <v-img :src="logo" alt="Restaurant logo"></v-img>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn text to="/">Home</v-btn>
    <v-btn text to="/orders">Orders</v-btn>
  </v-app-bar>
</template>

<script>
export default {
  data() {
    return {
      logo: 'path/to/logo.png'
    }
  }
}
</script>
