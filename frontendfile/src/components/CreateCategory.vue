<template>
    <div>
      <h1 class="mt-4">Create Category</h1>
      <form @submit.prevent="createcategory">
        <div class="form-group">
          <label for="categoryname">Category Name:</label>
          <input
            type="text"
            id="categoryname"
            v-model="categoryname"
            class="form-control"
            required
          />
        </div>
        <div class="form-group">
          <button type="submit" class="btn btn-primary">Create Category</button>
        </div>
      </form>
      <div class="text-center dashboard-btn" style="position: absolute; top: 20px; right: 20px;">
      <h2 class="heading"></h2>
      <router-link to="/adminlogout" class="btn btn-primary">Logout</router-link>
    </div>
    </div>
  </template>
  <script>

  import axios from 'axios';
  export default {
    data() {
      return {
        categoryname: "",
        userrole: JSON.parse(localStorage.getItem('user'))[0],
      };
    },
  
    methods: {
      createcategory() {
        if (this.userrole.role === "admin") {
          let formData = new FormData();
          const access_token = localStorage.getItem('access_token');
          formData.append('data', JSON.stringify(this.categoryname));
  
          axios.post("http://127.0.0.1:5000/createcategory", formData, {
            mode: 'cors',
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          })
            .then((response) => {
              if (response.status === 201) {
                console.log("Category created successfully");
                window.alert("Category created successfully");
                this.categoryname = "";
              } else {
                console.error("Error creating category");
              }
            })
            .catch((error) => {
              
              console.error("Error creating category", error);
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
  body {
    background-color: #f8f9fa; 
    padding: 20px;
  }
  
  h1 {
    color: #007bff; 
  }
    form {
    background-color: #fff; 
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.2);
  }
  
  
  label {
    font-weight: bold;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  button[type="submit"] {
    background-color: #007bff; 
    color: #fff; 
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
  }
  
  
  input[type="text"] {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  </style>
  