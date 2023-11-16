<template>
    <div>
      <input type="file" ref="fileInput" @change="handleFileChange" />
      <button @click="uploadFile">Upload</button>
      <div v-if="selectedFile">
        <h3>Selected File:</h3>
        <p>{{ selectedFile.name }}</p>
      </div>
      <div v-if="uploadResponse">
        <h3>Upload Response:</h3>
        <p>Filename: {{ uploadResponse.filename }}</p>
        <p>Saved Path: {{ uploadResponse.saved_path }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        selectedFile: null,
        uploadResponse: null,
      };
    },
    methods: {
      handleFileChange(event) {
        this.selectedFile = event.target.files[0];
      },
      async uploadFile() {
        if (this.selectedFile) {
          try {
            const formData = new FormData();
            formData.append('file', this.selectedFile);
  
            const response = await axios.post('http://127.0.0.1:8000/upload', formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization' : `Bearer ${localStorage.getItem('access_token')}`
              },
            });

            this.selectedFile = null;
            this.uploadResponse = response.data;
            this.$refs.fileInput.value = '';
            console.log('File uploaded:', this.uploadResponse);
          } catch (error) {
            console.error('Error uploading file:', error);
          }
        } else {
          console.error('No file selected');
        }
      },
    },
  };
  </script>
  