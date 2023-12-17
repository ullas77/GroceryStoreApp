<template>
    <div>
      <h1 class="text-success">Add to Cart</h1>
      <form @submit.prevent="addtocart">
        <div class="form-group">
          <label for="quantity">Please enter Quantity to purchase</label>
          <input
            type="text"
            id="quantity"
            v-model="quantity"
            class="form-control"
            required
          />
        </div>
        <button type="submit" class="btn btn-success">Add to cart</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        quantity: '',
        userrole: JSON.parse(localStorage.getItem('user'))[0],
      };
    },
    methods: {
      addtocart() {
        const access_token = localStorage.getItem('access_token');

        const productname = this.$route.params.productname;
        const formData = new FormData();
        formData.append('quantity', this.quantity); // Send 'quantity' as form data
  
        axios
          .post(`http://127.0.0.1:5000/addtocart/${productname}`, formData,{
            mode: 'cors',
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          })
          .then((response) => {
            if (response.status === 200) {
              console.log('Product added to cart successfully');
              window.alert('Product added to cart successfully');
              this.quantity = '';
              this.$router.push('/userlogin')
            } 
           
          })
          .catch((error) => {
            console.error('Error purchasing product', error);
          });
      },
    },
  };
  </script>
  