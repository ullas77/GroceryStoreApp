<template>
    <div class="products-list">
      <h2 class="text-center mt-4">List of Products</h2>
  
      <!-- Display Products -->
      <div v-if="products.length > 0">
        <ul class="product-ul">
          <li v-for="product in products" :key="product.productname" class="product-item">
            {{ product.productname }}
          </li>
        </ul>
      </div>
  
      <!-- Display a message when no products are found -->
      <div v-if="products.length === 0" class="no-products">
        <p>No products found.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  export default {
    data() {
      return {
        products: [],
      };
    },
    created() {
      // Fetch the list of products from the Flask API when the component is created
      this.fetchProducts();
    },
    methods: {
      fetchProducts() {
        // Make a GET request to the Flask API to fetch the list of products
        axios.get('http://127.0.0.1:5000/listproducts',{
            mode: 'cors',
           
          })
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
    },
  };
  </script>
  
  <style scoped>
  /* Custom styles for the products list with blue and white theme */
  .products-list {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #ffffff; /* White background */
    font-family: 'Arial', sans-serif; /* Specify your preferred font-family */
  }
  
  .product-ul {
    list-style: none;
    padding: 0;
  }
  
  .product-item {
    background-color: #3498db; /* Blue background */
    margin: 5px 0;
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    color: #ffffff; /* White text color */
    font-size: 16px; /* Specify your preferred font size */
    font-weight: bold; /* Bold font weight */
    text-align: center; /* Center text */
  }
  
  .product-item:hover {
    background-color: #2980b9; /* Darker blue on hover */
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); /* Add shadow on hover */
  }
  
  .no-products {
    margin-top: 20px;
    text-align: center;
    color: #888;
    font-style: italic; /* Specify your preferred font style */
  }
  </style>
  