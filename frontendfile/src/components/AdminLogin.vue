<template>
  <div class="container">
    <h1 class="heading" style="font-size: 50px;">Category Management</h1>

    <div class="card">
      <h2 class="heading">Create a new Category</h2>
      <router-link to="/createcategory" class="btn btn-primary">Create Category</router-link>
    </div>

    <div class="card">
      <h2 class="heading">Edit and Delete Categories</h2>
      <ul class="list-group">
        <li v-for="cat in categories" :key="cat.categoryname" class="list-group-item d-flex justify-content-between align-items-center">
          {{ cat.categoryname }}
          <div>
            <router-link :to="'/editcategory/' + cat.categoryname" class="btn btn-primary mr-2">Edit</router-link>
            <router-link :to="'/deletecategory/' + cat.categoryname" class="btn btn-secondary">Delete</router-link>
          </div>
          
        </li>
      </ul>
    </div>
    
<div class="card">
  <router-link to="/admindashboard" class="btn btn-primary">Admin Dashboard</router-link>

  
</div>
<div class="card">
      <h2 class="heading">Store Manager Category Change Requests</h2>
      <router-link to="/storemanagerrequests" class="btn btn-info">Store Manager Requests</router-link>
    </div>
    <div class="card">
      <h2 class="heading">New Store Manager Addition Requests</h2>
      <router-link to="/newsrequest" class="btn btn-info">New Store Manager Addition Requests</router-link>
    </div>
<div class="text-center dashboard-btn" style="position: absolute; top: 20px; right: 20px;">
      <h2 class="heading"></h2>
      <router-link to="/adminlogout" class="btn btn-primary">Logout</router-link>
    </div>
  </div>
 
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      categories: [],
    };
  },
  created() {
    this.fetchCategories();
  },
  methods: {
    fetchCategories() {
      axios.get('http://localhost:5000/listcategories')
        .then((response) => {
          if (response.data && response.data.categories) {
            this.categories = response.data.categories;
          } else {
            // Handle empty or invalid response data here
          }
        })
        .catch((error) => {
          console.error('Error fetching categories:', error);
        });
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
