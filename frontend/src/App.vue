<template>
  <div id="app">
    <input type="file" ref="fileInput" @change="handleFileChange" />
    <button @click="uploadFile">Upload</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
    };
  },
  methods: {
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    uploadFile() {
      const formData = new FormData();
      formData.append("file", this.selectedFile);

      this.$axios
        .post("http://localhost:8000/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          console.log(response.data);
          this.$refs.fileInput.value = null;
          this.selectedFile = null;
        })
        .catch((error) => {
          console.error("Error uploading file:", error);
        });
    },
  },
};
</script>

<style>
#app {
  text-align: center;
  margin-top: 60px;
}
</style>
