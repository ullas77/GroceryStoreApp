<template>
    <div>
      <h1>Category Request</h1>
      <form @submit.prevent="sendRequest">
        <div class="form-group">
          <label for="option">Request Option:</label>
          <select v-model="option" class="form-control" required>
            <option value="create">Create Category</option>
            <option value="edit">Edit Category</option>
            <option value="delete">Delete Category</option>
          </select>
        </div>

        <div class="form-group">
          <label for="categor">Category Name:</label>
          <input type="text" id="categor" v-model="categor" class="form-control" required>
        </div>
        <div class="text-center dashboard-btn" style="position: absolute; top: 20px; right: 20px;">
      <h2 class="heading"></h2>
      <router-link to="/storemanagerlogout" class="btn btn-primary">Logout</router-link>
    </div>
        <div class="form-group">
          <label for="modification" v-if="option === 'edit'">Modification Details:</label>
          <textarea id="modification" v-model="modification" class="form-control" rows="4" v-if="option === 'edit' "></textarea>
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
        option: 'create',
        categor: '',
        modification: '',
      };
    },
    methods: {
        
      sendRequest() {
        const access_token = localStorage.getItem('access_token');

        const requestData = {
          option: this.option,
          categor: this.categor,
          modification: this.modification,
        };
        axios.post('http://127.0.0.1:5000/storemanagerlogin/request', requestData,{
            mode: 'cors',
            headers: {
              Authorization: `Bearer ${access_token}`,
            },})
          .then((response) => {
            if (response.status === 201) {
              
              this.option = 'create';
              this.categor = '';
              this.modification = '';
              alert('Request sent successfully');
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
  