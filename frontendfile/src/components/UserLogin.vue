<template>
  <div>
    <div class="container">
      <h2 class="text-center mt-4">Search Products and categories</h2>
      <form @submit.prevent="searchProducts" class="mt-3">
        <div class="row">
          <div class="col-md-4">
            <label for="searchby">Search By:</label>
            <select v-model="searchBy" class="form-control" name="searchBy">
              <option value="productname">Product Name</option>
              <option value="categoryname">Category Name</option>
              <option value="rateperunit">Rate per unit</option>
              <option value="manufacturingdate">Manufacturing Date(yyyy-mm-dd)</option>
              <option value="expirydate">Expiry Date(yyyy-mm-dd)</option>

            </select>
          </div>
          <div class="col-md-4">
            <label for="searchterm">Search Term:</label>
            <input type="text" v-model="searchTerm" class="form-control" required>
          </div>
          <div class="col-md-4 d-flex align-items-end">
            <button type="submit" class="btn btn-primary mt-2">Search</button>
          </div>
        </div>
      </form>
    </div>
    <div class="row mt-4">
      <div class="col-md-6">
        <button @click="listProducts" class="btn btn-success btn-block">List of Products</button>
      </div>
      <div class="col-md-6">
        <button @click="listCategories" class="btn btn-info btn-block">List of Categories</button>
      </div>
    </div>

    <div class="row mt-4">
      <div class="col-md-6">
      <button @click="redirectToUserDashboard" class="btn btn-warning btn-block">User Purchases</button>
      </div>
    <div class="col-md-6">
      <button @click="redirectToCartItems" class="btn btn-secondary btn-block">User Cart</button>
      </div>
      </div>
      <div class="text-center dashboard-btn" style="position: absolute; top: 20px; right: 20px;">
      <h2 class="heading"></h2>
      <router-link to="/userlogout" class="btn btn-primary">Logout</router-link>
    </div>

    </div>
  
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchBy: '',
      searchTerm: '',
      searchResults: [], // Add searchResults to your data
      
    };
  },
  methods: {
    searchProducts() {
      // Make a POST request to the Flask backend with search criteria
      axios.post('http://127.0.0.1:5000/searchresults', {
    searchby: this.searchBy,
    searchterm: this.searchTerm,
  })
  .then((response) => {
    // Handle the response and update the searchResults data
    localStorage.setItem("searchby", this.searchBy);



    this.searchResults = response.data || [];
    

    // Navigate to the search results page with the search criteria
    this.$router.push({
      path: '/searchresults', // Route path
      
      query: {
        searchby: this.searchBy,
        searchterm: this.searchTerm,
      },
    });
  })
  .catch((error) => {
    console.error('Error searching:', error);
  });

        
    },

    listProducts() {
      // Redirect to the list of products page
      this.$router.push('/listproducts');
    },
    listCategories() {
      // Redirect to the list of categories page
      this.$router.push('/listcategories');
    },
    redirectToUserDashboard() {
      // Redirect to the user dashboard page
      this.$router.push('/userdashboard');
    },
    redirectToCartItems() {
      // Redirect to the user's cart page
      this.$router.push('/cartitems');
    },
  },
};
</script>

<style scoped>
/* Custom styles can be added here */
</style>
