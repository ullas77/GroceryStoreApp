<template>
  <div class="container">
    <section class="category-section">
      <h1 class="section-title">Categories</h1>
      <ul class="category-list">
        <li v-for="cat in categories" :key="cat.categoryid" class="category-item">
          {{ cat.categoryname }}
        </li>
      </ul>
      <div v-if="categories.length === 0" class="no-data-message">No categories found.</div>
    </section>

    <section class="product-section">
      <h1 class="section-title">Products</h1>
      <ul class="product-list">
        <li v-for="pro in products" :key="pro.productid" class="product-item">
          {{ pro.productname }}
        </li>
      </ul>
      <div v-if="products.length === 0" class="no-data-message">No products found.</div>
    </section>
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
      products: [], // Initialize products as an empty array
      categories: [], // Initialize categories as an empty array
      userrole: JSON.parse(localStorage.getItem('user'))[0],
    };
  },
  created() {
    this.fetchProducts();
    if (this.userrole.role === "admin") {
      this.fetchCategories();
    }
  },
  methods: {
    fetchProducts() {
      const access_token = localStorage.getItem('access_token');
      if (this.userrole.role === "admin") {
        axios.get('http://127.0.0.1:5000/listproducts', {
          mode: 'cors',
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
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
      } else {
        console.log("Unauthorised Access");
        window.alert("Unauthorised Access!!");
      }
    },
    fetchCategories() {
      const access_token = localStorage.getItem('access_token');
      axios.get('http://127.0.0.1:5000/listcategories', {
        mode: 'cors',
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      })
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
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f5f5f5;
  font-family: Arial, sans-serif;
  color: #333;
}

.section-title {
  color: #007bff;
  margin-bottom: 20px;
}

.category-section, .product-section {
  margin-bottom: 30px;
}

.category-list, .product-list {
  list-style: none;
  padding: 0;
}

.category-item, .product-item {
  background-color: #ffffff;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin: 10px 0;
  padding: 15px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 18px;
  font-weight: bold;
}

.category-item:hover, .product-item:hover {
  background-color: #f0f0f0;
}

.no-data-message {
  text-align: center;
  font-style: italic;
}
</style>
