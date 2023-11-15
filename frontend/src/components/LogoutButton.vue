<template>
    <div>
      <h2>Logout</h2>
      <button @click="logout">Logout</button>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    methods: {
      logout() {
        axios
          .post("http://127.0.0.1:8000/logout", {
            user_id: 1, // Replace with the actual user ID
          })
          .then(response => {
            console.log(response.data.message);
          })
          .catch(error => {
            console.error("Logout error:", error.response.data.detail);
          });
      },
    },
  };
  </script>
  
  <style scoped>
    /* Your component styles here */
  </style>
  