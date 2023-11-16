<template>
    <v-container>
      <div v-if="isLoggedIn" class="loggedIn">
        <v-container>
          <p class="welcome-message">Welcome, {{ username }}!</p>
          <UploadsForms />
        </v-container>
      </div>
  
      <div v-else class="notLoggedIn">
        <v-container>
          <p class="welcome-message">Hey, Welcome New User! Wanna try out ArbCSV?</p>
          <v-card class="auth-card">
            <v-btn color="success" @click="register">Register</v-btn>
            <v-btn color="info" @click="login">Login</v-btn>
          </v-card>
        </v-container>
      </div>
    </v-container>
  </template>
  
  <script>
  import { jwtDecode } from 'jwt-decode';
  import axios from 'axios';
  import UploadsForms from './UploadsForms.vue';
  
  export default {
    components: {
      UploadsForms,
    },
    data() {
      return {
        isLoggedIn: this.$store.getters.isLoggedIn,
        username: '',
      };
    },
    created() {
      const access_token = localStorage.getItem('access_token');
      if (this.isLoggedIn && access_token) {
        try {
          const decodedToken = jwtDecode(access_token);
          const userId = decodedToken.sub;
          this.getUsername(userId);
        } catch (error) {
          console.log(error);
        }
      }
    },
    methods: {
      login() {
        if (this.$route.path !== '/login') {
          this.$router.push('/login');
        }
      },
      register() {
        if (this.$route.path !== '/register') {
          this.$router.push('/register');
        }
      },
      getUsername(userId) {
        axios.get(`http://127.0.0.1:8000/users/${userId}`)
          .then((response) => {
            const username = response.data;
            this.username = username;
          })
          .catch((error) => {
            console.error('Error fetching username:', error);
          });
      },
    },
  };
  </script>
  
  <style scoped>
  /* Styles resembling Apple's design */
 /* Styling for the container */
.v-container {
  max-width: 800px; /* Adjust width as needed */
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

/* Styling for the welcome message */
.welcome-message {
  font-size: 24px;
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

/* Styling for the logged-in section */
.loggedIn {
  background-color: #f0f0f0; /* Light gray background */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* Styling for the not logged-in section */
.notLoggedIn {
  background-color: #fff; /* White background */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* Styling for the authentication card */
.auth-card {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.auth-card v-btn {
  margin: 0 10px;
  text-transform: uppercase;
  font-weight: bold;
  border-radius: 5px;
}

.auth-card v-btn:hover {
  opacity: 0.8;
}

/* Example of adding a background image */
.auth-card {

  background-size: cover;
  background-position: center;
  color: #fff; /* Set text color for better visibility */
  padding: 30px;
  text-align: center;
}

  </style>
  