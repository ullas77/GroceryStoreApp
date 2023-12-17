import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import './plugins/bootstrap-vue'
import './plugins/bootstrap-vue'
import App from './App.vue'
//import router from './router'
import VueRouter from 'vue-router'
import UllasKumar from './components/UllasKumar.vue'
import EditCategory from './components/EditCategory.vue'
import CreateCategory from './components/CreateCategory.vue'
import DeleteCategory from './components/DeleteCategory.vue'
import CreateProduct from './components/CreateProduct.vue'
import EditProduct from './components/EditProduct.vue'
import PurchaseProduct from './components/PurchaseProduct.vue'
import AddToCart from './components/AddToCart.vue'
import SalesAnalysis from './components/SalesAnalysis.vue'
import CartAnalysis from './components/CartAnalysis.vue'



import DeleteProduct from './components/DeleteProduct.vue'
import AdminLogin from './components/AdminLogin.vue'
import UserLogin from './components/UserLogin.vue'
import ListCategories from './components/ListCategories.vue'
import ListProducts from './components/ListProducts.vue'
import UserCart from './components/UserCart.vue'
import UserDashboard from './components/UserDashboard.vue'
import AdminDashboard from './components/AdminDashboard.vue'

import StoreManagerLogin from './components/StoreManagerLogin.vue'
import SearchResults from './components/SearchResults.vue'
import UserLogout from './components/UserLogout.vue'
import AdminLogout from './components/AdminLogout.vue'
import StoreManagerLogout from './components/StoreManagerLogout.vue'
import StoreManagerRequests from './components/StoreManagerRequests.vue'
import NewStoreManager from './components/NewStoreManager.vue'

import RequestCategory from './components/RequestCategory.vue'

import NewSRequest from './components/NewSRequest.vue'






Vue.use(VueRouter);
const routes=[
  {
    path:'/',
    component:UllasKumar
  },
  {
    path:'/newstoremanager',
    component:NewStoreManager
  },
  {
    path:'/newsrequest',
    component:NewSRequest
  },
  {
    path:'/storemanagerrequests',
    component:StoreManagerRequests
  },
  {
    path:'/storemanagerlogin/request',
    component:RequestCategory
  },
  {
    path:'/adminlogin',
    component:AdminLogin
  },
  {
    path:'/salesanalysis',
    component:SalesAnalysis
  },
  {
    path:'/cartanalysis',
    component:CartAnalysis
  },
  {
    path:'/adminlogout',
    component:AdminLogout
  },
  {
    path:'/searchresults',
    component:SearchResults
  },
  {
    path:'/storemanagerlogout',
    component:StoreManagerLogout
  },
  {
    path:'/userlogout',
    component:UserLogout
  },
  {
    path:'/admindashboard',
    component:AdminDashboard
  },
  {
    path:'/userdashboard',
    component:UserDashboard
  },
  {
    path:'/userlogin',
    component:UserLogin
  },
  {
    path:'/listcategories',
    component:ListCategories
  },
  {
    path:'/cartitems',
    component:UserCart
  },
  
  {
    path:'/listproducts',
    component:ListProducts
  },
  
{
  path:'/editcategory/:categoryname',
component:EditCategory
},
{
  path:'/createcategory',
component:CreateCategory
},
{
  path:'/deletecategory/:categoryname',
component:DeleteCategory
},
{
  path:'/editproduct/:productname',
component:EditProduct
},
{
  path:'/purchase/:productname',
component:PurchaseProduct
},
{
  path:'/addtocart/:productname',
component:AddToCart
},
{
  path:'/createproduct',
component:CreateProduct
},
{
  path:'/deleteproduct/:productname',
component:DeleteProduct
},
{
  path:'/storemanagerlogin',
component:StoreManagerLogin
},




]
const router=new VueRouter({
  routes
})
Vue.config.productionTip = false

new Vue({
  router:router,
  render: h => h(App),
}).$mount('#app')

