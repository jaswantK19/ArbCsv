<template>
  <v-container>
    <v-card class="login-card">
      <v-card-title>
        <h1>Login</h1>
      </v-card-title>
      <v-card-text>
        <v-form class="login-form">
          <v-text-field v-model="email" type="email" label="Email" prepend-icon="mdi-email-box" class="input-field" />
          <v-text-field v-model="password" :type="showPassword ? 'text' : 'password'" label="Password" prepend-icon="mdi-lock"
            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" @click:append="showPassword = !showPassword"
            class="input-field" />
        </v-form>
      </v-card-text>
      <v-divider class="divider" />
      <v-card-actions>
        <span class="card-actions">
  
            <v-btn color="success" @click="login">Login</v-btn>
         
          <div class="new-user-message">New User? <router-link to="/register"> Register</router-link></div>
        </span>
      </v-card-actions>
    </v-card>
  </v-container>
</template>
  
  <script>
  
  export default {
    data() {
      return {
        email: "",
        password: "",
        showPassword: false
      };
    },
    methods: {
      login() {
        this.$store.dispatch('auth/login', {
        email: this.email,
        password: this.password,
    })
      }
    },
  };
  </script>
  

  <style scoped>
  .login-card {
    max-width: 400px;
    margin: auto;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .login-form {
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    align-items: stretch;
  }
  
  .input-field {
    margin-bottom: 15px;
  }
  
  .divider {
    margin: 20px 0;
  }
  
  .card-actions {
    display: flex;
    flex-direction: row;
    align-items: center;
  }
  
  .new-user-message {
    margin-top: 10px;
    margin-left: 10px;
    font-size: 14px;
    color: #888;
  }
  
  /* Additional styles can be added here */
  </style>
  