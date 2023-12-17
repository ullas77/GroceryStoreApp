<template>
  <div>
    <h2 class="text-center mt-4">Products</h2>

    <!-- Display Products -->
    <!-- <div v-if="searchby === 'productname'"> -->
      <table class="table">
        <thead>
          <tr>
            <th>ProductID</th>
            <th>ProductName</th>
            <th>Rate per unit</th>
            <th>Manufacturing Date</th>
            <th>Expiry date</th>
            <th>Purchase this Product</th>
            <th>Add to Cart</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.productname">
            <td>{{ product.productid }}</td>
            <td>{{ product.productname }}</td>
            <td>{{ product.rateperunit }}</td>
            <td>{{ product.manufacturingdate }}</td>
            <td>{{ product.expirydate }}</td>
            <td><router-link :to="'/purchase/' + product.productname" class="btn btn-primary mr-2">Purchase this Product</router-link></td>
            <td><router-link :to="'/addtocart/' + product.productname" class="btn btn-primary mr-2">Add to Cart</router-link></td>


          </tr>
        </tbody>
      </table>
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
      products: [],
      categories: [],
      searchby:localStorage.getItem('searchby'),
      searchterm:'',
      
    };
  },
  created() {
    this.searchProducts();
  },
  methods: {
    searchProducts() {
      const searchby = this.$route.query.searchby;
      const searchterm = this.$route.query.searchterm;

      if (searchby && searchterm) {
        axios
          .post('http://127.0.0.1:5000/searchresults', {
            searchby,
            searchterm,
          })
          .then((response) => {
            if (response.data) {
              this.products = response.data.products;
              this.categories = response.data.categories;
              
            } else {
              // Handle empty or invalid response data here
            }
          })
          .catch((error) => {
            console.error('Error searching products:', error);
          });
      } else {
        // No search query parameters, fetch all products
      }
    },
    
  },
};


</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  padding: 12px;
  text-align: center;
}

th {
  background-color: #4CAF50;
  color: white;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}

a {
  color: #ffffff;
  text-decoration: none;
}

a:hover {
  color: #06e023;
}</style>
