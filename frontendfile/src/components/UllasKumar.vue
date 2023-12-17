<template>
    <div class="container" style="background-image: url('/o.png');">

    <h1 class="box" >GROCERY STORE APP</h1>
    <h2 class="heading">Login for User, Admin, and Store Manager</h2>

    <div class="row">
      <div class="col-md-6">
        <h3 class="heading">User Signup</h3>
        <form @submit.prevent="userSignup" class="form-container">
          <div class="form-group">
            <label for="username" class="form-label">Username</label>
            <input type="text" id="username" v-model="username" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="password" class="form-label">Password</label>
            <input type="password" id="password" v-model="password" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="useremail" class="form-label">UserEmail</label>
            <input type="email" id="useremail" v-model="useremail" class="form-control" required>
          </div>
          <div class="form-group">
            <button type="submit" class="btn btn-secondary">Register</button>
          </div>
        </form>
      </div>
      <div class="col-md-6">
        <h3 class="heading">Login</h3>
        <form @submit.prevent="userLogin" class="form-container">
         <div class="form-group">
            <label for="loginusername" class="form-label">Name</label>
            <input type="text" id="loginusername" v-model="loginusername" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="loginpassword" class="form-label">Password</label>
            <input type="password" id="loginpassword" v-model="loginpassword" class="form-control" required>
          </div>
          <div class="form-group">
            <button type="submit" class="btn btn-secondary">Login</button>
          </div>
        </form>
      </div>
    </div>
    <router-link to="/newstoremanager" class="btn btn-secondary">Apply as Store Manager</router-link>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      username: "",
      password: "",
      useremail: "",
      loginusername: "",
      loginpassword: ""
    };
  },
  methods: {
    userSignup() {
      const formData = {
        username: this.username,
        password: this.password,
        useremail: this.useremail
      };
      axios.post('http://127.0.0.1:5000/signup', formData)
        .then(() => {
           
          window.alert("User Registered Successfully, Now u can log in using your crediantials");
          this.username='',
          this.password= '',
          this.useremail=''
          
        })
        .catch((error) => {
          console.error('Error Sign up', error);
        });
    },
    userLogin() {
      const formData = {
        username: this.loginusername,
        password: this.loginpassword,
      };
      axios.post('http://127.0.0.1:5000/login', formData)
        .then((response) => {
          const user = response.data.user
          console.log(user[0].role);
          if (this.loginusername === "admin") {
            const accessToken = response.data.access_token;
            localStorage.setItem("access_token", accessToken);
            const user = response.data.user;
            localStorage.setItem("user", JSON.stringify(user));
            this.$router.push('/adminlogin');
          }
          else if(user[0].role=="storemanager") {
            const accessToken = response.data.access_token;
            localStorage.setItem("access_token", accessToken);
            const user = response.data.user;
            localStorage.setItem("user", JSON.stringify(user));
            this.$router.push('/storemanagerlogin');
          }
          
          else{
            const accessToken = response.data.access_token;
            localStorage.setItem("access_token", accessToken);
            const user = response.data.user;
            localStorage.setItem("user", JSON.stringify(user));
            this.$router.push('/userlogin');
          }
        })
        .catch((error) => {
          console.error('Error logging in', error);
          window.alert("Bad Credentials")
        });
    },
  },
};
</script>

<style scoped>
/* Add your custom styles here if needed */
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f5f5f5;
  background-size: cover
}
.box {
  background-color: rgba(255, 255, 255, 0.807);
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: center;
  max-width: 600px;
  position: relative;
  top: 80%;
  left: 50%;
  transform: translate(-50%, -20%);
  font-weight: bold;
}

.heading-box {
  font-size: 36px;
  font-weight: bold;
  color: #333;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  margin: 20px 0;
}

.heading {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
  font-weight: bold;

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
  background-color: #0a0a0a;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  
}

.btn-secondary {
  background-color: #0b0a0a;
}

.btn:hover {
  background-color: #0056b3;
}
</style>
