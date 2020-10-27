

<template>
    <el-carousel indicator-position="outside" height="400px">
      <el-carousel-item v-for="(value,index) in banner_list" :key="value.id">
        <a :href="value.link">
          <!-- router-link 站内跳转 -->
          <!-- a标签 站外跳转 -->
          <img :src="value.image_url" alt="" style="width: 100%;height: 400px;">
<!--          <img src="@/assets/banner1.png" alt="">-->
        </a>
      </el-carousel-item>
    </el-carousel>



</template>

<script>


export default {
  name: "Banner",
  data(){
    return {
      banner_list:[

      ]
    }

  },
  methods:{
    get_banner_data(){
      this.$axios.get(`${this.$settings.Host}/home/banner`)
        .then((res)=>{
          console.log(res);
          this.banner_list = res.data;
        })
      .catch((error)=>{

      })
    }
  },
  created(){
    this.get_banner_data();
  },




}
</script>

<style scoped>

</style>
