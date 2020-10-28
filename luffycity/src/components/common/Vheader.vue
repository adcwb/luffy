<template>
  <div class="total-header">
    <div class="header">
      <el-container>
        <el-header height="80px" class="header-cont">
          <el-row>
            <el-col class="logo" :span="3">
              <a href="/">
                <img src="@/assets/header-logo.svg" alt="">

              </a>
            </el-col>
            <el-col class="nav" :span="10">
              <el-row>
                <el-col :span="3" v-for="(value,index) in nav_data_list" :key="index">

                  <a :href="value.link" class="active" v-if="value.is_site">{{value.title}}</a>

                  <router-link :to="value.link" v-else>{{value.title}}</router-link>

                </el-col>

              </el-row>

            </el-col>
            <el-col :span="11" class="header-right-box">
              <div class="search">
                <input type="text" id="Input" placeholder="请输入想搜索的课程" style="" @blur="inputShowHandler" ref="Input"
                       v-show="!s_status">
                <ul @click="ulShowHandler" v-show="s_status" class="search-ul" ref="xx">
                  <span>Python</span>
                  <span>Linux</span>
                </ul>
                <p>
                  <img class="icon" src="@/assets/sousuo1.png" alt="" v-show="s_status">
                  <img class="icon" src="@/assets/sousuo2.png" alt="" v-show="!s_status">
                  <img class="new" src="@/assets/new.png" alt="">
                </p>
              </div>
              <div class="register" v-show="!token">
                <router-link to="/user/login">
                  <button class="signin">登录</button>
                </router-link>
                &nbsp;&nbsp;|&nbsp;&nbsp;
                <a target="_blank" href="https://www.luffycity.com/signup">
                  <router-link to="/register">
                    <button class="signup">注册</button>
                  </router-link>

                </a>
              </div>
              <div class="shop-car" v-show="token">
                <router-link to="/cart">
                  <b>6</b>
                  <img src="@/assets/shopcart.png" alt="">
                  <span>购物车 </span>
                </router-link>
              </div>
              <div class="nav-right-box" v-show="token">
                <div class="nav-right">
                  <router-link to="/myclass">
                    <div class="nav-study">我的教室</div>
                  </router-link>
                  <div class="nav-img" @mouseover="personInfoList" @mouseout="personInfoOut">
                    <img src="@/assets/touxiang.png" alt="" style="border: 1px solid rgb(243, 243, 243);">
                    <ul class="home-my-account" v-show="list_status" @mouseover="personInfoList">

                      <li>
                        我的账户
                        <img src="https://hcdn2.luffycity.com/media/frontend/activity/back_1568185800.821227.svg"
                             alt="">
                      </li>
                      <li>
                        我的订单
                        <img src="https://hcdn2.luffycity.com/media/frontend/activity/back_1568185800.821227.svg"
                             alt="">
                      </li>
                      <li>
                        贝里小卖铺
                        <img src="https://hcdn2.luffycity.com/media/frontend/activity/back_1568185800.821227.svg"
                             alt="">
                      </li>
                      <li>
                        我的优惠券
                        <img src="https://hcdn2.luffycity.com/media/frontend/activity/back_1568185800.821227.svg"
                             alt="">
                      </li>
                      <li>
                    <span>
                      我的消息
                      <b>(26)</b>
                    </span>
                        <img src="https://hcdn2.luffycity.com/media/frontend/activity/back_1568185800.821227.svg"
                             alt="">
                      </li>
                      <li @click="logout">
                        退出
                        <img src="https://hcdn2.luffycity.com/media/frontend/activity/back_1568185800.821227.svg"
                             alt="">
                      </li>

                    </ul>
                  </div>

                </div>

              </div>


            </el-col>
          </el-row>

        </el-header>


      </el-container>

    </div>
  </div>

</template>

<script>
export default {
  name: "Vheader",
  data() {
    return {

      token: false, // 登录成功与否的标记
      s_status: true, // 放大镜效果切换控制,默认input标签不显示
      list_status: false, // 个人中心下拉菜单是否显示

      nav_data_list:[],
    }
  },
  created(){
    this.get_nav_data();
    this.check_login();
  },
  methods: {
    ulShowHandler() {
      // console.log(this);
      this.s_status = false;
      console.log(this.$refs);a

      this.$nextTick(function () {
        console.log(this);
        this.$refs.Input.focus();
      });


    },
    inputShowHandler() {
      this.s_status = true;
    },
    personInfoList() {
      this.list_status = true;
    },
    personInfoOut() {
      this.list_status = false;
    },

    get_nav_data(){
      this.$axios.get(`${this.$settings.Host}/home/nav/top/`)
      .then((res)=>{
        this.nav_data_list = res.data;
      })
    },

    check_login(){
      this.token = localStorage.token || sessionStorage.token;
      //console.log(this.token);
    },
    // 退出登录
    logout(){

      sessionStorage.removeItem('token');
      sessionStorage.removeItem('username');
      sessionStorage.removeItem('id');
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      localStorage.removeItem('id');
      console.log('xxxxxx')
      this.check_login();
      // this.token = false;
    }

  }
}


</script>

<style scoped>
.header-cont .nav .active {
  color: #f5a623;
  font-weight: 500;
  border-bottom: 2px solid #f5a623;
}

.total-header {
  min-width: 1200px;
  z-index: 100;
  box-shadow: 0 4px 8px 0 hsla(0, 0%, 59%, .1);
}

.header {
  width: 1200px;
  margin: 0 auto;
}

.header .el-header {
  padding: 0;
}

.logo {
  height: 80px;
  /*line-height: 80px;*/
  /*text-align: center;*/
  display: flex; /* css3里面的弹性布局，高度设定好之后，设置这个属性就能让里面的内容居中 */
  align-items: center;
}

.nav .el-row .el-col {
  height: 80px;
  line-height: 80px;
  text-align: center;

}

.nav a {
  font-size: 15px;
  font-weight: 400;
  cursor: pointer;
  color: #4a4a4a;
  text-decoration: none;
}

.nav .el-row .el-col a:hover {
  border-bottom: 2px solid #f5a623
}

.header-cont {
  position: relative;
}

.search input {
  width: 185px;
  height: 26px;
  font-size: 14px;
  color: #4a4a4a;
  border: none;
  border-bottom: 1px solid #ffc210;

  outline: none;
}

.search ul {
  width: 185px;
  height: 26px;
  display: flex;
  align-items: center;
  padding: 0;

  padding-bottom: 3px;
  border-bottom: 1px solid hsla(0, 0%, 59%, .25);
  cursor: text;
  margin: 0;
  font-family: Helvetica Neue, Helvetica, Microsoft YaHei, Arial, sans-serif;
}

.search .search-ul, .search #Input {
  padding-top: 10px;
}

.search ul span {
  color: #545c63;
  font-size: 12px;
  padding: 3px 12px;
  background: #eeeeef;
  cursor: pointer;
  margin-right: 3px;
  border-radius: 11px;
}

.hide {
  display: none;
}

.search {
  height: auto;
  display: flex;
}

.search p {
  position: relative;
  margin-right: 20px;
  margin-left: 4px;
}

.search p .icon {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.search p .new {
  width: 18px;
  height: 10px;
  position: absolute;
  left: 15px;
  top: 0;
}

.register {
  height: 36px;
  display: flex;
  align-items: center;
  line-height: 36px;
}

.register .signin, .register .signup {
  font-size: 14px;
  color: #5e5e5e;
  white-space: nowrap;
}

.register button {
  outline: none;
  cursor: pointer;
  border: none;
  background: transparent;
}

.register a {
  color: #000;
  outline: none;
}

.header-right-box {
  height: 100%;
  display: flex;
  align-items: center;
  font-size: 15px;
  color: #4a4a4a;
  position: absolute;
  right: 0;
  top: 0;
}

.shop-car {
  width: 99px;
  height: 28px;
  border-radius: 15px;
  margin-right: 20px;
  background: #f7f7f7;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  cursor: pointer;
}

.shop-car b {
  position: absolute;
  left: 28px;
  top: -1px;
  width: 18px;
  height: 16px;
  color: #fff;
  font-size: 12px;
  font-weight: 350;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  background: #ff0826;
  overflow: hidden;
  transform: scale(.8);
}

.shop-car img {
  width: 20px;
  height: 20px;
  margin-right: 7px;
}

.nav-right-box {
  position: relative;
}

.nav-right-box .nav-right {
  float: right;
  display: flex;
  height: 100%;
  line-height: 60px;
  position: relative;
}

.nav-right .nav-study {
  font-size: 15px;
  font-weight: 300;
  color: #5e5e5e;
  margin-right: 20px;
  cursor: pointer;

}

.nav-right .nav-study:hover {
  color: #000;
}

.nav-img img {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: inline-block;
  cursor: pointer;
}

.home-my-account {
  position: absolute;
  right: 0;
  top: 60px;
  z-index: 101;
  width: 190px;
  height: auto;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 4px 8px 0 #d0d0d0;
}

li {
  list-style: none;
}

.home-my-account li {
  height: 40px;
  font-size: 14px;
  font-weight: 300;
  color: #5e5e5e;
  padding-left: 20px;
  padding-right: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-sizing: border-box;
}

.home-my-account li img {
  cursor: pointer;
  width: 5px;
  height: 10px;
}

.home-my-account li span {
  height: 40px;
  display: flex;
  align-items: center;
}

.home-my-account li span b {
  font-weight: 300;
  margin-top: -2px;
}


</style>

