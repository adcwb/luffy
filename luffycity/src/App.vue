<template>
  <div id="app">

    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  created() {
    //监听页面刷新事件，将数据保存到sessionStorage中
    window.addEventListener('beforeunload',()=>{
      console.log('页面要刷新啦！！！,赶紧保存数据！！！！');
      sessionStorage.setItem('cart_length',this.$store.state.cart_length);
    })

  }
}
</script>

<style>


body{
    margin: 0;
    padding: 0;
  }
  ul{
    list-style: none;
    padding: 0;
    margin: 0;
  }
  li{
    list-style: none;
  }
  /*.el-header{*/
  /*  width: 1200px;*/
  /*}*/
  input,select,textarea{
    border: none;
    outline: none;
  }
  a{
    text-decoration: none;
    color: #4a4a4a;
  }

</style>
