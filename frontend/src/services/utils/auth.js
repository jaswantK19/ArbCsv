import axios from "axios";


export function setAuthHeaders() {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
      } else {
        delete axios.defaults.headers.common['Authorization'];
      }
}