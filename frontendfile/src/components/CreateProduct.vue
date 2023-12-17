<template>
  <div class="container">
    <h1 class="mt-4 text-primary">Create Product</h1>
    <form @submit.prevent="createProduct" class="mt-3">
      <div class="form-group">
        <label for="productname" class="font-weight-bold">Product Name:</label>
        <input type="text" class="form-control" v-model="product.productname" required>
      </div>
      <div class="form-group">
        <label for="rateperunit" class="font-weight-bold">Rate per Unit:</label>
        <input type="number" step="0.01" class="form-control" v-model="product.rateperunit" required>
      </div>
      <div class="form-group">
        <label for="manufacturingdate" class="font-weight-bold">Manufacturing Date:</label>
        <input type="date" class="form-control" v-model="product.manufacturingdate" required>
      </div>
      <div class="form-group">
        <label for="expirydate" class="font-weight-bold">Expiry Date:</label>
        <input type="date" class="form-control" v-model="product.expirydate" required>
      </div>
      <div class="form-group">
        <label for="maxquantity" class="font-weight-bold">Max Quantity(Stock):</label>
        <input type="number" class="form-control" v-model="product.maxquantity" required>
      </div>
      <div class="form-group">
        <label for="categoryid" class="font-weight-bold">Category:</label>
        <select class="form-control" v-model="product.categoryid" required>
          <option v-for="category in categories" :key="category.categoryid" :value="category.categoryid">{{ category.categoryname }}</option>
        </select>
      </div>
      <div class="form-group">
        <button type="submit" class="btn btn-primary">Create Product</button>
      </div>
    </form>
    <div class="text-center dashboard-btn" style="position: absolute; top: 20px; right: 20px;">
      <h2 class="heading"></h2>
      <router-link to="/storemanagerlogout" class="btn btn-primary">Logout</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userrole: JSON.parse(localStorage.getItem('user'))[0],
      product: {
        productname: '',
        rateperunit: '',
        manufacturingdate: '',
        expirydate: '',
        maxquantity: '',
        categoryid: '', // Use an array to store selected categories
      },
      categories: [], // Populate this with your category data
      selectedCategory: null, // Initialize selectedCategory
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
    
    createProduct() {
      // if (this.selectedCategory) {
        // this.product.categories.push(this selectedCategory);
      if (this.userrole.role === "admin" || this.userrole.role === "storemanager") {
        const data = {
          productname: this.product.productname,
          rateperunit: this.product.rateperunit,
          manufacturingdate: this.product.manufacturingdate,
          expirydate: this.product.expirydate,
          maxquantity: this.product.maxquantity,
          categoryid: this.product.categoryid
          // .map((category) => category.categoryid),
        };
        const access_token = localStorage.getItem('access_token');


        axios.post('http://localhost:5000/createproduct', data, {
          mode: 'cors',
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        })
          .then((response) => {
            if (response.status === 201) {
              console.log('Product created successfully');
              window.alert('Product created successfully');
              this.$router.push('/storemanagerlogin'); 
            } else {
              console.error('Error creating product');
            }
          })
          .catch((error) => {
            console.error('Error creating product', error);
          });
      } else {
        console.log("Unauthorised Access");
        window.alert("Unauthorised Access!!");
      }
    }
  }
};

</script>
<style scoped>
  /* Add your custom styles here */
  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f5f5f5;
  }

  .heading {
    font-size: 24px;
    margin-bottom: 20px;
    color: #333;
  }

  .form-container {
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin: 10px;
  }

  .form-label {
    font-weight: bold;
    display: block;
    margin-bottom: 5px;
  }

  .form-group {
    margin-bottom: 15px;
  }

  .form-control {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }

  .btn {
    padding: 10px 20px;
    font-size: 16px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  .btn-secondary {
    background-color: #333;
  }

  .btn:hover {
    background-color: #0056b3;
  }
</style>


