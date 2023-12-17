<template>
  <div id="app">
   
    <router-view></router-view>

  </div>
</template>

<script>



export default {
  name: 'App',

  components: {
    
  },
  data(){
    return {title:"Props Titorial"}
  },
  methods:{
    updateTitle(title){
      this.title=title
    }
  }
}
</script>

<style lang="scss">
@import "~@/assets/scss/vendors/bootstrap-vue/index";
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
