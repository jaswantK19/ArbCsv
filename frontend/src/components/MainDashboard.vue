<template>
    <v-container>
        <div class="loggedIn" v-if="this.$store.getters.isLoggedIn">
            <v-container>
                Welcome {{ username }} !

                <v-container>
                    <UploadsForms />
                </v-container>
            </v-container>
        </div>

        <div class="notLoggedIn" v-if="this.$store.getters.isLoggedIn !== 'true'">
            <v-container>
                Hey Welcome New User ! Wanna try out ArbCSV ?
                <v-card>
                    <v-btn color="success" @click="register"> Register</v-btn>
                    <v-btn color="info" @click="login"> Login</v-btn>
                </v-card>
            </v-container>
        </div>
    </v-container>
</template>

<script>
import {jwtDecode} from 'jwt-decode'
import axios from 'axios'
import UploadsForms from './UploadsForms.vue'

    export default {
        
        components: {
    UploadsForms,

},
        
        data() {
            return {
                isLoggedIn : this.$store.getters.isLoggedIn,
                username: ""
            } 
        },
        created() {
            console.log("Component is Created!")
            const access_token = localStorage.getItem('access_token')
            console.log(access_token)
            console.log(this.isLoggedIn)
            if (this.isLoggedIn && access_token){
                try {
                    const decodedToken = jwtDecode(access_token)
                    const userId = decodedToken.sub
                    this.getUsername(userId)
                    
                } catch (error) {
                    console.log(error)
                    
                }
            }
        },

        methods : {

        login() {
            if (this.$route.path !== '/login'){
                this.$router.push('/login');
            }
        },

        register() {
            if (this.$route.path !== '/register'){
                this.$router.push('/register');
            }
        },

        getUsername(userId) {
            axios.get(`http://127.0.0.1:8000/users/${userId}`)
            .then((response) => {
                const username = response.data
                this.username = username
            })
        }
    }
}
</script>