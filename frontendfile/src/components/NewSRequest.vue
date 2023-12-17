<template>
    <div>
      <h1>Admin Dashboard</h1>
      <!-- <div v-if="storemanagerequest.length === 0">
        <p>No pending requests</p>
      </div>
      <div v-else> -->
        <h2>Pending Requests</h2>
        <table class="table">
          <thead>
            <tr>
              <th>Store Manager</th>
              <th>Email</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in storemanagerrequest" :key="request.id">
              <td>{{ request.name }}</td>
              <td>{{ request.email }}</td>
              <td>
                <button @click="approveReq(request.id)" class="btn btn-success">Approve</button>
                <button @click="rejectReq(request.id)" class="btn btn-danger">Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    <!-- </div> -->
  </template>
  
  <script>
  import axios from 'axios'
  export default {
    data() {
      return {
        storemanagerrequest: [],
        userrole: JSON.parse(localStorage.getItem('user'))[0], // Populate this array with your requests data
      };
    },
    created() {
      this.fetchnew();
    },
    methods: {
        fetchnew() {
        if (this.userrole.role === "admin") {
          const access_token = localStorage.getItem('access_token');
          axios.get('http://127.0.0.1:5000/newsrequest', {
            mode: 'cors',
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          })
            .then((response) => {
              if (response.data && response.data.requests) {
                this.storemanagerrequest = response.data.requests;
              } else {
                // Handle empty or invalid response data here
              }
            })
            .catch((error) => {
              console.error('Error fetching store manager requests:', error);
            });
        }
      },
      approveReq(reqid) {
        if (this.userrole.role === "admin") {
          const access_token = localStorage.getItem('access_token');
          axios.post(`http://127.0.0.1:5000/ap/${reqid}`, {
            mode: 'cors',
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          })
            .then((response) => {
              if (response.status === 200) {
                // Request approved successfully
                window.alert("Request approved successfully");
                this.fetchnew();
              } else {
                // Handle error response
              }
            })
            .catch((error) => {
              console.error('Error approving request:', error);
            });
        }
      },
      rejectReq(reqid) {
        if (this.userrole.role === "admin") {
          const access_token = localStorage.getItem('access_token');
          axios.post(`http://127.0.0.1:5000/re/${reqid}`, {
            mode: 'cors',
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          })
            .then((response) => {
              if (response.status === 200) {
                this.fetchnew();
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
  