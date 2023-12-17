<template>
    <div>
      <h1>New Store Manager Registration</h1>
      <form @submit.prevent="sendRequest">
        <div class="form-group">
          <label for="storemanagerName">Name:</label>
          <input type="text" id="storemanagerName" v-model="storemanagerName" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="storemanagerPassword">Password:</label>
          <input type="password" id="storemanagerPassword" v-model="storemanagerPassword" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="storemanagerEmail">Email:</label>
          <input type="email" id="storemanagerEmail" v-model="storemanagerEmail" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary">Send Request</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        storemanagerName: '',
        storemanagerPassword: '',
        storemanagerEmail: '',
      };
    },
    methods: {
      sendRequest() {
        const requestData = {
          name: this.storemanagerName,
          password: this.storemanagerPassword,
          email: this.storemanagerEmail,
        };
  
        axios.post('http://127.0.0.1:5000/newstoremanager', requestData)
          .then((response) => {
            if (response.status === 201) {
              this.storemanagerName = '';
              this.storemanagerPassword = '';
              this.storemanagerEmail = '';
              window.alert('Request sent successfully, After admin approves ,you can login as a Store Manager');
              // You can navigate to a different route upon success.
              // this.$router.push('/success'); // Replace '/success' with the desired route
            } else {
              alert('Error sending the request');
            }
          })
          .catch((error) => {
            alert('Error sending the request: ' + error);
          });
      },
    },
  };
  </script>
  