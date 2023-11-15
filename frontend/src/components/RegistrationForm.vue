<template>
  <v-container>
    <v-card class="registration-card">
      <v-card-title>
        <h1>Registration</h1>
      </v-card-title>

      <v-card-text>
        <v-form class="registration-form">
          <v-text-field v-model="name" label="Username" prepend-icon="mdi-account-circle" class="input-field" />
          <v-text-field v-model="email" type="email" label="Email" prepend-icon="mdi-email-box" class="input-field" />
          <v-text-field v-model="password" :type="showPassword ? 'text' : 'password'" label="Password" prepend-icon="mdi-lock"
            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" @click:append="showPassword = !showPassword"
            class="input-field" />
        </v-form>
      </v-card-text>

      <v-divider class="divider" />

      <v-card-actions>
        <span class="card-actions">
          <router-link to="/dashboard" @click.native="register">
            <v-btn class="register-btn" color="success">Register</v-btn>
          </router-link>

          <div class="registered-message">Already Registered? <router-link to="/login"> Login</router-link></div>
        </span>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      name: "",
      email: "",
      password: "",
      showPassword: false
    };
  },
  methods: {
    register() {
      axios
        .post("http://127.0.0.1:8000/register", {
          username: this.name,
          email: this.email,
          password: this.password,
        })
        .then((response) => {
          console.log(response.data.message);
        })
        .catch((error) => {
          console.error("Registration error:", error.response.data.detail);
        });
    },
  },
};
</script>

<style scoped>
.registration-card {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.registration-form {
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
  flex-direction: column;
  align-items: row;
}

.register-button {
  padding: 10px;
  margin: 10px;
}

.registered-message {
  margin-top: 10px;
  margin-left: 10px;
  font-size: 14px;
  color: #888;
}

/* Add more styles as needed */
</style>
