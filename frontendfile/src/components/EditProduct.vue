<template>
  <div>
    <h1 class="text-success">Edit Product</h1>
    <form @submit.prevent="updateProduct">
      <div class="form-group">
        <label for="newvname">Please enter new Product Name</label>
        <input
          type="text"
          id="newvname"
          v-model="newvname"
          class="form-control"
          required
        />
      </div>
      <button type="submit" class="btn btn-success">Update</button>
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
      newvname: '',
      userrole: JSON.parse(localStorage.getItem('user'))[0],
    };
  },
  methods: {
    updateProduct() {
      if (this.userrole.role === "admin" || this.userrole.role === "storemanager") {
        const productname = this.$route.params.productname;
        const formData = new FormData();
        const access_token = localStorage.getItem('access_token');

        formData.append('data', JSON.stringify(this.newvname));

        axios
          .post(`http://127.0.0.1:5000/editproduct/${productname}`, formData, {
            mode: 'cors',
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          })
          .then((response) => {
            if (response.status === 201) {
              console.log('Product edited successfully');
              window.alert('Product edited successfully');
              this.$router.push('/storemanagerlogin');
              this.newvname = '';
            } else {
              console.error('Error editing product');
            }
          })
          .catch((error) => {
            console.error('Error editing product', error);
          });
      } else {
        console.log("Unauthorised Access");
        window.alert("Unauthorised Access!!");
      }
    },
  },
};
</script>
