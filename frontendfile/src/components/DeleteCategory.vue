<template>
  <div>
    <h1 class="text-danger">Are you sure of Deleting this Category?</h1>
    <p>Category Name: {{ categoryname }}</p>
    <button @click="deleteCategory" class="btn btn-danger">Delete</button><div class="text-center dashboard-btn">
      <div class="text-center dashboard-btn" style="position: absolute; top: 20px; right: 20px;">
      <h2 class="heading"></h2>
      <router-link to="/adminlogout" class="btn btn-primary">Logout</router-link>
    </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      categoryname: this.$route.params.categoryname,
      userrole: JSON.parse(localStorage.getItem('user'))[0],
    };
  },
  methods: {
    deleteCategory() {
      if (this.userrole.role === "admin") {
        const access_token = localStorage.getItem('access_token');
        axios
          .post(`http://127.0.0.1:5000/deletecategory/${this.categoryname}`, null, {
            mode: 'cors',
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          })
          .then((response) => {
            if (response.status === 200) {
              console.log("Category deleted successfully");
              this.$router.push('/adminlogin');
            } else {
              console.error("Error deleting category");
            }
          })
          .catch((error) => {
            console.error("Error deleting category", error);
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
  /* Custom styles for the Delete Category page */
  body {
    background-color: #f8f9fa; /* Light gray background */
    padding: 20px;
  }

  h2 {
    color: #007bff; /* Blue header text */
  }

  /* Style the form container */
  form {
    background-color: #fff; /* White background for the form */
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.2);
  }

  /* Style the submit button */
  button[type="submit"] {
    background-color: #007bff; /* Blue submit button */
    color: #fff; /* White text color */
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
  }
</style>
