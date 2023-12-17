<template>
    <div class="cart-list">
      <h2 class="text-center mt-4">List of Products</h2>
  
      <div v-if="cartitems.length > 0">
        <ul class="product-ul">
          <li v-for="product in cartitems" :key="product.productname" class="cart-item">
            <div class="product-info">
              <div class="product-name">{{ product.productname }}</div>
              <div class="product-quantity">{{ product.quantity }} units</div>
            </div>
          </li>
        </ul>
      </div>
  
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
        cartitems: [],
        userrole: JSON.parse(localStorage.getItem('user'))[0],
      };
    },
    created() {
      this.fetchCart();
    },
    methods: {
      fetchCart() {
        const access_token = localStorage.getItem('access_token');

        axios.get('http://127.0.0.1:5000/cartitems',{
            mode: 'cors',
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          })
          .then((response) => {
            if (response.data && response.data.cartitems) {
              this.cartitems = response.data.cartitems;
            } else {
              // Handle empty or invalid response data here
            }
          })
          .catch((error) => {
            console.error('Error fetching cartitems:', error);
          });
      },
    },
  };
  </script>
  
  <style scoped>
  /* Custom styles for the products list in the cart with enhanced styling */
  
  .cart-list {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f2f2f2; /* Light gray background */
    font-family: 'Helvetica Neue', sans-serif; /* Specify your preferred font-family */
  }
  
  .product-ul {
    list-style: none;
    padding: 0;
  }
  
  .cart-item {
    background-color: #4CAF50; /* Green background */
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
  
  .cart-item:hover {
    background-color: #45A049; /* Darker green on hover */
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); /* Add shadow on hover */
  }
  
  .product-info {
    display: flex;
    flex-direction: column;
  }
  
  .product-name {
    font-size: 20px; /* Larger font size for product names */
  }
  
  .product-quantity {
    font-size: 16px; /* Font size for product quantities */
    color: #555; /* Dark gray text color for quantities */
  }
  
  .no-products {
    margin-top: 20px;
    text-align: center;
    color: #888; /* Dark gray text color */
    font-style: italic; /* Italic font style */
    font-size: 20px; /* Larger font size for the message */
  }
  </style>
  