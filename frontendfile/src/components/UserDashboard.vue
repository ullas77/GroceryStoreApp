<template>
    <div class="cart-list">
      <h2 class="text-center mt-4">List of Products Purchased</h2>
  
      <!-- Display Products -->
      <div v-if="purchaseditems.length > 0">
        <ul class="product-ul">
          <li v-for="product in purchaseditems" :key="product.productname" class="product-item">
            <div class="product-info">
              <div class="product-name">{{ product.productname }}</div>
              <div class="product-quantity">{{ product.quantity }} units</div>
            </div>
          </li>
        </ul>
      </div>
  
      <!-- Display a message when no products are found -->
      <div v-else class="no-products">
        <p>No products found.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        purchaseditems: [],
        userrole: JSON.parse(localStorage.getItem('user'))[0],      };
    },
    created() {
      this.UserDashboard();
      this.userid = localStorage.getItem('userid')
    },
    methods: {
      UserDashboard() {
        const access_token = localStorage.getItem('access_token');

        axios.get('http://127.0.0.1:5000/userdashboard',{
            mode: 'cors',
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          })
          .then((response) => {
            if (response.data && response.data.purchaseditems) {
              this.purchaseditems = response.data.purchaseditems;
            } else {
              // Handle empty or invalid response data here
            }
          })
          .catch((error) => {
            console.error('Error fetching purchaseditems', error);
          });
      },
    },
  };
  </script>
  
  <style scoped>
  /* Custom styles for the products list with enhanced styling */
  
  .cart-list {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f7f7f7; /* Light gray background */
    font-family: 'Arial', sans-serif; /* Specify your preferred font-family */
  }
  
  .product-ul {
    list-style: none;
    padding: 0;
  }
  
  .product-item {
    background-color: #3498db; /* Blue background */
    margin: 10px 0;
    padding: 15px;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    color: #ffffff; /* White text color */
    font-size: 18px; /* Larger font size */
    font-weight: bold; /* Bold font weight */
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'Roboto', sans-serif; /* Specify a Google Font or your preferred font */
  }
  
  .product-item:hover {
    background-color: #2980b9; /* Darker blue on hover */
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); /* Add shadow on hover */
  }
  
  .product-info {
    display: flex;
    flex-direction: column;
  }
  
  .product-name {
    font-size: 24px; /* Larger font size for product name */
  }
  
  .product-quantity {
    font-size: 18px; /* Larger font size for quantity */
    color: #ddd;
  }
  
  .no-products {
    margin-top: 20px;
    text-align: center;
    color: #555; /* Dark gray text color */
    font-style: italic; /* Italic font style */
    font-size: 20px; /* Larger font size for the message */
  }
  </style>
  