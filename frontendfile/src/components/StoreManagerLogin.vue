<template>
    <div class="container">
      <h1 class="heading" style="font-size: 50px;">Product Management</h1>
  
      <div class="card">
        <h2 class="heading">Create a new Product</h2>
        <router-link to="/createproduct" class="btn btn-primary">Create Product</router-link>
      </div>
  
      <div class="card">
        <h2 class="heading">Edit and Delete Products</h2>
        <ul class="list-group">
          <li v-for="pro in products" :key="pro.productname" class="list-group-item d-flex justify-content-between align-items-center">
            {{ pro.productname }}
            <div>
              <router-link :to="'/editproduct/' + pro.productname" class="btn btn-primary mr-2">Edit</router-link>
              <router-link :to="'/deleteproduct/' + pro.productname" class="btn btn-secondary">Delete</router-link>
            </div>
          </li>
        </ul>
      </div>
      <div class="text-center dashboard-btn" style="position: absolute; top: 20px; right: 20px;">
      <h2 class="heading"></h2>
      <router-link to="/storemanagerlogout" class="btn btn-primary">Logout</router-link>
    </div>
    <div class="card" >
      <h2 class="heading">List of Categories</h2>
      <router-link to="/listcategories" class="btn btn-primary">List of Categories</router-link>
      </div>
      <div class="card">
       
    <button @click="triggerCeleryJob" class="btn btn-primary">Export as csv.</button>
  </div>

    <div class="card">
        <h2 class="heading">Create Request</h2>
        <router-link to="/storemanagerlogin/request" class="btn btn-primary">Create Request</router-link>
      </div>

      <div class="card">
        <router-link to="/salesanalysis" class="btn btn-primary">Sales Analysis</router-link>

       
     </div>
     <div class="card">
        <router-link to="/cartanalysis" class="btn btn-primary">Cart Analysis</router-link>

       
     </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        products: [],
        userrole: JSON.parse(localStorage.getItem('user'))[0]
      };
    },
    created() {
      this.fetchProducts();
    },
    methods: {
      fetchProducts() {
        axios.get('http://localhost:5000/listproducts')
          .then((response) => {
            if (response.data && response.data.products) {
              this.products = response.data.products;
            } else {
              // Handle empty or invalid response data here
            }
          })
          .catch((error) => {
            console.error('Error fetching products:', error);
          });
      },
      triggerCeleryJob() {
      if (this.userrole.role === "storemanager"){
      const access_token = localStorage.getItem('access_token');

      axios.post('http://127.0.0.1:5000/trigger_celery_job', null, {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      })
        .then((response) => {
          this.taskInfo = response.data;
          window.alert("CSV file is generated successfully")
        })
        .catch((error) => {
          console.error('Error triggering Celery job:', error);
        });
      } else {
        console.log("Unauthorised Access");
        window.alert("Unauthorised Access!!");
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
  
  .btn-primary {
    background-color: #007bff;
    border-color: #007bff;
  }
  
  .btn-primary:hover {
    background-color: #0056b3;
    border-color: #0056b3;
  }
  
  .btn-secondary {
    background-color: #6c757d;
    border-color: #6c757d;
  }
  
  .btn-secondary:hover {
    background-color: #565e64;
    border-color: #565e64;
  }
  </style>
  