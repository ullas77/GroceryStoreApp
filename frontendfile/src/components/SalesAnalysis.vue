<template>
    <div>
      <h1>Sales Analysis</h1>
      <img :src="chartImage" alt="Sales Chart" />
      <div class="text-center dashboard-btn" style="position: absolute; top: 20px; right: 20px;">
      <h2 class="heading"></h2>
      <router-link to="/storemanagerlogout" class="btn btn-primary">Logout</router-link>
    </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        chartImage: null,
        userrole: JSON.parse(localStorage.getItem('user'))[0],
      };
    },
    created() {
      this.fetchSalesChart();
    },
    methods: {
      fetchSalesChart() {
        if (this.userrole.role === "storemanager") {
          const access_token = localStorage.getItem('access_token');
  
          axios.get('http://127.0.0.1:5000/salesanalysis', {
            mode: 'cors',
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
            responseType: 'blob', // Set the response type to blob
          })
          .then((response) => {
            const blob = new Blob([response.data], { type: 'image/png' });
            this.chartImage = URL.createObjectURL(blob);
          })
          .catch((error) => {
            console.error('Error fetching sales chart:', error);
          });
        } else {
          window.alert("Unauthorised Access");
        }
      },
    },
  };
  </script>
  