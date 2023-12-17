<template>
    <div class="container">
      <h1 class="heading">User Logout</h1>
      <button @click="UserLogout" class="btn btn-secondary">Logout</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      UserLogout() {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");
  
        this.$router.push("/");
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
    }
  
    .heading {
      font-size: 24px;
      margin-bottom: 20px;
      color: #333;
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
  
    .btn:hover {
      background-color: #0056b3;
    }
  </style>
  