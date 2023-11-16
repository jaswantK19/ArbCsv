import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex)

export const store = new Vuex.Store(
    {
        state: {
            loggedIn: localStorage.getItem('loggedIn')
        },

        mutations: {
            SET_LOGIN_STATE(state, payload) {
                state.loggedIn = payload

            },
            LOGOUT(state) {
                state.loggedIn = false;
            }
        },
        actions: {
            login({ commit }, { email, password }) {
                return new Promise((resolve, reject) => {
                  axios
                    .post("http://127.0.0.1:8000/login", {
                      email,
                      password,
                    })
                    .then(response => {
                      const { access_token, refresh_token } = response.data;
                      localStorage.setItem('access_token', access_token);
                      localStorage.setItem('refresh_token', refresh_token);
                      localStorage.setItem('loggedIn', true);
                      commit('SET_LOGIN_STATE', localStorage.getItem('loggedIn')); 
                      console.log(localStorage.getItem('loggedIn'))
                      resolve();
                    })
                    .catch(error => {
                      console.error("Login error:", error.response);
                      reject(error);
                    });
                });
              },
            logout({commit}) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('loggedIn');
                
                commit('LOGOUT'); 
            },

            register({ commit }, { username, email, password }) {
              return new Promise((resolve, reject) => {
                axios
                  .post("http://127.0.0.1:8000/register", {
                    username,
                    email,
                    password,
                  })
                  .then(
                    commit('login', { email, password }),
                    resolve()
                  )
                  .catch(error => {
                    console.error("Login error:", error.response);
                    reject(error);
                  });
              });
            },
    

        },

        getters: {
            isLoggedIn: state => state.loggedIn
            // other getters
          }
    }
)