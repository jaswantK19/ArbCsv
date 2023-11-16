<template>
    <v-container>
      <v-list>
        <v-list-item v-for="item in uploadsList" :key="item.upload_id" class="list-item">
          <v-list-item-content @click="navigate(item)">
            <v-list-item-title>{{ item.name }}</v-list-item-title>
            <v-list-item-subtitle>ID: {{ item.upload_id }}</v-list-item-subtitle>
          </v-list-item-content>
          <v-list-item-action>
            <v-btn color="primary" @click.stop="editFile(item)" class="action-button">
              Edit
            </v-btn>
            <v-btn color="error" @click="deleteFile(item.upload_id)" class="action-button">
              Delete
            </v-btn>
          </v-list-item-action>
        </v-list-item>
      </v-list>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        uploadsList: [],
      };
    },
    methods: {
      async getUploads() {
        try {
          const response = await axios.get('http://127.0.0.1:8000/getUploads', {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
          });
          return response.data; // Return response data, not the response object itself
        } catch (error) {
          console.error('Error fetching uploads:', error);
          throw error; // Propagate the error up
        }
      },
      async editFile(file) {

        console.log('Editing file:', file);
      },
      async deleteFile(uploadId) {
            try {
                const response = await axios.delete(`http://127.0.0.1:8000/delete/${uploadId}`);
                console.log('File deleted:', response.data);
                const index = this.uploadsList.findIndex(item => item.upload_id === uploadId);
    
                if (index !== -1) {
               
                this.uploadsList.splice(index, 1);
                }
             
            } catch (error) {
                console.error('Error deleting file:', error);
            }
      },
      async navigate(item) {
        console.log('Navigating to:', item);
      },
    },
    async created() {
      try {
        this.uploadsList = await this.getUploads();           
      } catch (error) {
        console.log(error)
      }
    },
  };
  </script>
  
  <style scoped>
  .list-item {
  border-bottom: 1px solid #ccc;
  padding: 15px;
  transition: background-color 0.3s ease-in-out;
}

.list-item:hover {
  background-color: #f0f0f0;
}

.action-button {
  margin-right: 8px;
  min-width: 60px;
  text-transform: uppercase;
  font-weight: bold;
}

  </style>
  