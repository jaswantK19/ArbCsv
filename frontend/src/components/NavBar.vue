<template>
  <v-container fluid>
    <v-navigation-drawer v-model="drawer" app >
      <v-list v-if="loggedIn" dense>
        <v-list-item v-for="(item, index) in items" :key="index" @click="navigate(item)">
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
      <v-list v-else dense>
        <v-list-item v-for="(item, index) in itemsWhenNotLoggedIn" :key="index" @click="navigate(item)">
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title class="ml-4">My App</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="loggedIn" @click="handleLogout">Logout</v-btn>
      <v-btn v-else @click="login">Login</v-btn>
    </v-app-bar>
  </v-container>
</template>

<script>
import { mapActions } from 'vuex';
export default {
  data() {
    return {
      drawer: false, 
      items: [
        { title: 'Home', icon: 'mdi-home', path: '/dashboard' },
        { title: 'Uploads', icon: 'mdi-cloud-upload', path: '/uploads' }
      ],
      itemsWhenNotLoggedIn: [
        {title: 'Home', icon: 'mdi-home', path: '/Sdashboard'},
        {title: 'About us', icon: 'mdi-information', path: '/about'}
      ]
    };
  },
  computed : {
        loggedIn() {
          return this.$store.getters.isLoggedIn
        }
    },
  methods: {
    navigate(item) {
        if (this.$route.path !== item.path) {
      
        this.$router.push(item.path);
    }
    },
    login() {
      if (this.$route.path !== '/login'){
        this.$router.push('/login');
      }
    },
    ...mapActions(['logout']),
    handleLogout() {
      this.logout()
      if (this.$route.path !== '/dashboard'){
        
        this.$router.push('/dashboard');
      }
      else{
        this.$router.go()
      }
    }
  }
};
</script>

<style scoped>

.v-navigation-drawer,
.v-app-bar {
  background-color: rgba(84, 66, 248, 0.3)}

.v-btn {
  color: #fff; /* Text color for buttons */
}

.v-list-item:hover {
  background-color: #e0e0e0; /* Hover color for list items */
}
/* Your custom styles here */
</style>