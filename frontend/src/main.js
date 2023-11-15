import Vue from 'vue'
import App from './App.vue'
import vuex
import axios from 'axios';
import VueRouter from 'vue-router';
import Routes from './routes';
import vuetify from './plugins/vuetify'

Vue.use(VueRouter)

const router = new VueRouter({
  routes: Routes

})



Vue.config.productionTip = false
Vue.prototype.$axios = axios;

new Vue({
  render: h => h(App),
  vuetify,
  router: router
}).$mount('#app')
