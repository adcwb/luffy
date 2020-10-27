<template>
  <div class="home">

    <Vheader></Vheader>
    <Banner></Banner>
    <Footer></Footer>

  </div>

</template>

<script>
import Vheader from '@/components/common/Vheader'
import Banner from '@/components/common/Banner'
import Footer from '@/components/common/Footer'

export default {
  name: "Home",
  data(){
    return {
      title:'Home组件'
    }

  },
  components:{
    Vheader,
    Banner,
    Footer,
  }

}
</script>

<style scoped>
/* scoped  */
h1{
  color:red;
}

</style>
