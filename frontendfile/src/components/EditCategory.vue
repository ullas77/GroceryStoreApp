<template>
  <div>
    <h1 class="text-success">Edit Category</h1>
    <form @submit.prevent="updateCategory">
      <div class="form-group">
        <label for="newvname">Please enter a new Category</label>
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
      <router-link to="/adminlogout" class="btn btn-primary">Logout</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userrole: JSON.parse(localStorage.getItem('user'))[0],
      newvname: '',
    };
  },
  methods: {
    updateCategory() {
      if (this.userrole.role === "admin") {
        const categoryname = this.$route.params.categoryname;
        const formData = new FormData();
        const access_token = localStorage.getItem('access_token');
        formData.append('data', JSON.stringify(this.newvname));

        axios
          .post(`http://127.0.0.1:5000/editcategory/${categoryname}`, formData, {
            mode: 'cors',
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          })
          .then((response) => {
            if (response.status === 201) {
              console.log('Category edited successfully');
              window.alert('Category edited successfully');
              this.newvname = '';
              this.$router.push('/adminlogin')
            } else {
              console.error('Error editing category');
            }
          })
          .catch((error) => {
            console.error('Error editing category', error);
          });
      } else {
        console.log('Unauthorised Access');
        window.alert('Unauthorised Access');
      }
    },
  },
};
</script>
