<template>

    <v-container>
        <v-navigation-drawer v-model="drawer" app>
          <v-list>
            <v-list-item v-for="(item, index) in items" :key="index" @click="navigate(item)">
              <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-icon>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-navigation-drawer>
        <v-app-bar app>
          <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
          <v-toolbar-title>My App</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn v-if="isLoggedIn" @click="logout">Logout</v-btn>
          <v-btn v-else @click="login">Login</v-btn>
        </v-app-bar>
    </v-container>
</template>

<script>
export default {
  data() {
    return {
      drawer: false,
      isLoggedIn: localStorage.getItem('loggedIn'), // Change this based on user authentication status
      items: [
        { title: 'Home', icon: 'mdi-home', path: '/dashboard' },
        { title: 'Uploads', icon: 'mdi-cloud-upload', path: '/uploads' }
      ]
    };
  },
  methods: {
    navigate(item) {
        if (this.$route.path !== item.path) {
      
        this.$router.push(item.path);
    }
    },
    login() {
        this.$router.push('/login')
    },
    logout() {
      localStorage.delete('access_token', 'refresh_token', )
    }
  }
};
</script>

<style>
/* Your custom styles here */
</style>