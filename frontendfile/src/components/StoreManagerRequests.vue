<template>
    <div class="container">
      <h1 class="heading" style="font-size: 50px;">Store Manager Requests</h1>
  
      <div class="card">
        <h2 class="sub-heading">Requests from Store Managers</h2>
        <ul class="list-group">
          <li v-for="request in storeManagerRequests" :key="request.id" class="list-group-item">
            <div class="request-details">
              <p><strong>Storemanager ID:</strong> {{ request.storemanagerid }}</p>
              <p><strong> &nbsp; Request Task:</strong>  {{ request.option }}</p>
              <p><strong>Modification:</strong>  {{ request.categor }}</p>
              <p v-if="request.option === 'edit'"><strong>Modify to {{ request.modification }}</strong></p>

            </div>
            <div class="button-container">
              <button @click="approveRequest(request.id)" class="btn btn-success mr-2">Approve</button>
              <button @click="rejectRequest(request.id)" class="btn btn-danger">Reject</button>
            </div>
          </li>
        </ul>
      </div>
  
      <div class="text-center dashboard-btn" style="position: absolute; top: 20px; right: 20px;">
        <router-link to="/adminlogout" class="btn logout-button">Logout</router-link>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        storeManagerRequests: [],
        userrole: JSON.parse(localStorage.getItem('user'))[0],
      };
    },
    created() {
      this.fetchStoreManagerRequests();
    },
    methods: {
      fetchStoreManagerRequests() {
        if (this.userrole.role === "admin") {
          const access_token = localStorage.getItem('access_token');
          axios.get('http://127.0.0.1:5000/storemanagerrequests', {
            mode: 'cors',
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          })
            .then((response) => {
              if (response.data && response.data.requests) {
                this.storeManagerRequests = response.data.requests;
              } else {
                // Handle empty or invalid response data here
              }
            })
            .catch((error) => {
              console.error('Error fetching store manager requests:', error);
            });
        }
      },
      approveRequest(requestid) {
        if (this.userrole.role === "admin") {
          const access_token = localStorage.getItem('access_token');
          axios.post(`http://127.0.0.1:5000/approverequest/${requestid}`, {
            mode: 'cors',
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          })
            .then((response) => {
              if (response.status === 200) {
                // Request approved successfully
                window.alert("Request approved successfully");
                this.fetchStoreManagerRequests();
              } else {
                // Handle error response
              }
            })
            .catch((error) => {
              console.error('Error approving request:', error);
            });
        }
      },
      rejectRequest(requestid) {
        if (this.userrole.role === "admin") {
          const access_token = localStorage.getItem('access_token');
          axios.post(`http://127.0.0.1:5000/rejectrequest/${requestid}`, {
            mode: 'cors',
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          })
            .then((response) => {
              if (response.status === 200) {
                this.fetchStoreManagerRequests();
              } else {
                // Handle error response
              }
            })
            .catch((error) => {
              console.error('Error rejecting request:', error);
            });
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your scoped styles here */
  .heading {
    text-align: center;
    margin-bottom: 20px;
    color: #007bff;
    font-size: 24px;
  }
  
  .card {
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
    padding: 20px;
    margin-bottom: 20px;
  }
  
  .list-group {
    padding: 0;
  }
  
  .list-group-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
    font-size: 18px;
  }
  
  .btn-success {
    background-color: #28a745; /* Green color for "Approve" */
    border-color: #28a745;
  }
  
  .btn-success:hover {
    background-color: #218838;
    border-color: #218838;
  }
  
  .btn-danger {
    background-color: #dc3545; /* Red color for "Reject" */
    border-color: #dc3545;
  }
  
  .btn-danger:hover {
    background-color: #c82333;
    border-color: #c82333;
  }
  
  .logout-button {
    background-color: #007bff;
    border-color: #007bff;
  }
  </style>
  