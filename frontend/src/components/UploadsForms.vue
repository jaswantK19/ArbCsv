<template>
    <div class="file-upload">
      <label for="fileInput" class="file-input-label">
        <input type="file" id="fileInput" ref="fileInput" @change="handleFileChange" class="file-input" />
        <span class="choose-button">Choose File</span>
      </label>
      <button @click="uploadFile" class="upload-button">Upload</button>
  
      <div v-if="selectedFile" class="file-details">
        <h3>Selected File:</h3>
        <p>{{ selectedFile.name }}</p>
      </div>
  
      <div v-if="uploadResponse" class="upload-response">
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
  <style scoped>
    .file-upload {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

/* Style for file input label */
.file-input-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 15px;
}

.file-input {
  display: none;
}

.upload-button {
  padding: 10px 20px;
  background-color: #3498db;
  color: #fff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.choose-button {
  padding: 10px 20px;
  background-color: rgba(19, 240, 240, 0.4);
  color: #fff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.upload-button:hover {
  background-color: #2980b9;
}

/* Style for file details and upload response */
.file-details,
.upload-response {
  margin-top: 20px;
}

/* Heading styles */
h3 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #333;
}

/* Paragraph styles */
p {
  font-size: 16px;
  color: #555;
  margin-bottom: 5px;
}
</style>