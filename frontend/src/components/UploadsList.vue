<template>
    <v-container>
      <v-row v-if="uploadsList.length > 0">
        <v-col v-for="item in uploadsList" :key="item.upload_id" cols="12" md="6" lg="4">
          <v-card class="upload-card">
            <v-list-item @click="navigate(item)">
              <v-list-item-content>
                <v-list-item-title class="upload-title">{{ item.name }}</v-list-item-title>
                <v-list-item-subtitle>ID: {{ item.upload_id }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-card-actions>
              <v-btn color="success" @click="viewCSV(item.upload_id)" class="action-button success">
                View
              </v-btn>
              <v-btn color="primary" @click.stop="editFile(item)" class="action-button primary">
                Edit
              </v-btn>
              <v-btn color="error" @click="deleteFile(item.upload_id)" class="action-button error">
                Delete
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      <v-container v-else class="no-upload-container">
        No uploads yet!
      </v-container>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios';
  import Papa from 'papaparse';
  
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
          return response.data; 
        } catch (error) {
          console.error('Error fetching uploads:', error);
          throw error; 
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
      async viewCSV(uploadId) {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/viewFile/${uploadId}`, {
          responseType: 'text',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        });

        const parsedCSV = Papa.parse(response.data, {
          header: true, // Assuming CSV contains headers in the first row
        });

        // Create a new tab/window with a structured HTML table for the CSV data
        const newWindow = window.open('', '_blank');
        newWindow.document.write('<html><head><title>CSV Data</title></head><body>');

        // Create the HTML table structure
        newWindow.document.write('<table border="1">');
        
        // Add table headers
        newWindow.document.write('<thead><tr>');
        for (const header of parsedCSV.meta.fields) {
          newWindow.document.write(`<th>${header}</th>`);
        }
        newWindow.document.write('</tr></thead>');
        
        // Add table rows with data
        newWindow.document.write('<tbody>');
        for (const row of parsedCSV.data) {
          newWindow.document.write('<tr>');
          for (const field of parsedCSV.meta.fields) {
            newWindow.document.write(`<td>${row[field]}</td>`);
          }
          newWindow.document.write('</tr>');
        }
        newWindow.document.write('</tbody>');
        
        // Close the table and HTML structure
        newWindow.document.write('</table></body></html>');
        newWindow.document.close();

      } catch (error) {
        console.error('Error viewing file:', error);
        // Handle errors here, such as displaying an error message to the user
      }
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
 .upload-card {
  margin-bottom: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

/* Styles for upload titles */
.upload-title {
  font-size: 20px;
  color: #333;
}

/* Styles for action buttons */
.action-button {
  font-weight: bold;
  text-transform: uppercase;
  border-radius: 20px;
  padding: 8px 16px;
}

/* Button color variations */
.action-button.success {
  background-color: #4caf50;
  color: #fff;
}

.action-button.primary {
  background-color: #2196f3;
  color: #fff;
}

.action-button.error {
  background-color: #f44336;
  color: #fff;
}

/* Styles for no uploads container */
.no-upload-container {
  text-align: center;
  margin-top: 20px;
  font-size: 18px;
  color: #777;
}

  </style>
  