import axios from "axios";

export const state = {
    isLoggedIn: !!localStorage.getItem('loggedIn')
}

export const mutations = {
    LOGIN(state){
        state.isLoggedIn = true;
        localStorage.setItem('loggedIn', 'true')
    },
    LOGOUT(state) {
        state.isLoggedIn = false;
        localStorage.removeItem('loggedIn')
    }
}

export const actions = {
    login({ commit }, { email, password }) {
        return axios.post(`${process.env.VUE_APP_ROOT_URL}/login`, {
          email,
          password,
        })
        .then(response => {
          const { access_token, refresh_token } = response.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);
          commit('LOGIN'); // Commit the LOGIN mutation
          return response; // Return the response for any further handling in components
        })
        .catch(error => {
          console.error("Login error:", error.response.data.detail);
          throw error; // Propagate the error for handling in components
        });
      },

}