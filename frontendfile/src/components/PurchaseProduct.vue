<template>
    <div>
      <h1 class="text-success">Purchase product</h1>
      <form @submit.prevent="purchase">
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
        <button type="submit" class="btn btn-success">Purchase</button>
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
      purchase() {
        const productname = this.$route.params.productname;
        const access_token = localStorage.getItem('access_token');
        
        const formData = new FormData();
        formData.append('quantity', this.quantity); // Send 'quantity' as form data
  
        axios
          .post(`http://127.0.0.1:5000/purchase/${productname}`, formData,{
            mode: 'cors',
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          })
          .then((response) => {
            if (response.status === 200) {
              console.log('Product purchased successfully');
              const rateperunit=response.data.rateperunit
              const totalPrice = rateperunit * this.quantity
              const message = `Product purchased successfully.\nTotal Amount to be Paid: Rs.${totalPrice}`;
              window.alert(message)

              this.quantity = '';
              this.$router.push('/userlogin')
              
            } 
            if (response.status==201){
            window.alert('Sorry the product is out of stock')
;
            }
          })
          .catch((error) => {
            console.error('Error purchasing product', error);
          });
      },
    },
  };
  </script>
  