<template>
  <div class="login box">
    <img src="../../static/img/Loginbg.3377d0c.jpg" alt="">
    <div class="login">
      <div class="login-title">
        <img src="../../static/img/Logotitle.1ba5466.png" alt="">
        <p>帮助有志向的年轻人通过努力学习获得体面的工作和生活!</p>
      </div>
      <div class="login_box">
        <div class="title">
          <span @click="login_type=0">密码登录</span>
          <span @click="login_type=1">短信登录</span>
        </div>
        <div class="inp" v-if="login_type==0">
          <input v-model = "username" type="text" placeholder="用户名 / 手机号码" class="user">
          <input v-model = "password" type="password" name="" class="pwd" placeholder="密码">
          <div id="geetest1"></div>
          <div class="rember">
            <p>
              <input type="checkbox" class="no" name="a" v-model="remember"/>
              <span>记住密码</span>
            </p>
            <p>忘记密码</p>
          </div>
          <button class="login_btn" @click="loginHandle">登录</button>
          <p class="go_login" >没有账号 <span>立即注册</span></p>
        </div>
        <div class="inp" v-show="login_type==1">
          <input v-model = "mobile" type="text" placeholder="手机号码" class="user" @blur="checkPhone">
          <input v-model = "sms" type="text" placeholder="输入验证码" class="user" style="width: 62%">
          <button style="width: 34%;height: 41px;" @click="getSmsCode" :disabled="this.flag">{{btn_msg}}</button>
          <button class="login_btn">登录</button>
          <p class="go_login" >没有账号 <span>立即注册</span></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data(){
    return {
      login_type: 0,
      username:"",
      password:"",
      remember:false,
      sms:"",
      mobile:"",
      interval_time:60,  // 倒计时时间
      btn_msg:'点击获取验证码',
      flag:false,  // 判断定时器 是否已经开启
    }
  },

  methods:{
    checkPhone(){

      let phoneNumber = this.mobile;
      // 前端
      let reg = /^1[3-9][0-9]{9}$/;
      if (!reg.test(phoneNumber)){
        this.$message.error('手机号格式错误');
        return false;
      }
      // 发送请求
      this.$axios.get(`${this.$settings.Host}/users/check_phone/?phone=${phoneNumber}`)  // request.GET.get(phone)
        .then((res)=>{
          console.log(res);
        }).catch((error)=>{
        this.$message.error(error.response.data.error_msg);
      })

    },

    loginHandle(){
      // 判断手机号或者密码是否为空！
      if(this.username.length<1 || this.password.length<1){
        // 阻止代码继续往下执行
        return false;
      }

      var captcha1 = new TencentCaptcha('2021539286', (res) =>{
        if (res.ret === 0){

          /**
           用户操作验证码成功以后的回调函数，这个函数将会在对象创建以后，在页面那种进行监听用户的操作
           res就是用户操作成功以后，验证码服务器返回的内容

           res:
           appid: "2086888489"  # 验证码的APPID
           randstr: "@G0V"      # 随机字符串，防止重复
           ret: 0               # 0表示用户操作成功，2表示用户主动关闭验证码窗口
           ticket: ""           # 验证通过以后的票据，提供给python后端，将来到验证码服务器中进行
           */

          this.$axios.post(`${this.$settings.Host}/users/login/`,{
            username:this.username,
            password:this.password,
            ticket:res.ticket,
            randstr:res.randstr,

          }).then((res)=>{
            console.log(res);
            // console.log(this.remember);
            if (this.remember){
              localStorage.token = res.data.token;
              localStorage.username = res.data.username;
              localStorage.id = res.data.id;
              localStorage.credit = res.data.credit;
              localStorage.credit_to_money = res.data.credit_to_money;
              sessionStorage.removeItem('token');
              sessionStorage.removeItem('username');
              sessionStorage.removeItem('id');
              sessionStorage.removeItem('credit');
              sessionStorage.removeItem('credit_to_money');
            }else {
              sessionStorage.token = res.data.token;
              sessionStorage.username = res.data.username;
              sessionStorage.id = res.data.id;
              sessionStorage.credit = res.data.credit;
              sessionStorage.credit_to_money = res.data.credit_to_money;
              localStorage.removeItem('token');
              localStorage.removeItem('username');
              localStorage.removeItem('id');
              localStorage.removeItem('credit');
              localStorage.removeItem('credit_to_money');
            }

            this.$confirm('下一步想去哪消费！', '提示', {
              confirmButtonText: '去首页',
              cancelButtonText: '回到上一页',
              type: 'success'
            }).then(() => {
              this.$router.push('/');
            }).catch(() => {
              this.$router.go(-1);
            });


            }).catch((error)=>{
              this.$alert('用户名或者密码错误', '登录失败', {
                confirmButtonText: '确定',

            });
          })
        }
      });
      captcha1.show(); // 显示验证码



    },


    getSmsCode(){
      this.$axios.get(`${this.$settings.Host}/users/sms_code/${this.mobile}`)
      .then((res) => {
        if (!this.flag){
          this.flag = setInterval(() =>{
            if (this.interval_time > 0) {
              this.interval_time--;
              this.btn_msg = `${this.interval_time}秒后重新获取`;
            }
            else {
              this.interval_time = 60;
              this.btn_msg = '点击发送验证码'
              clearInterval(this.flag);
              this.flag = false;
            }
          },
            1000)
        }
      })
      .catch((error) => {
        this.$message.error(error.response.data.msg);
      })


    }

  },

};
</script>

<style scoped>
.box{
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}
.box img{
  width: 100%;
  min-height: 100%;
}
.box .login {
  position: absolute;
  width: 500px;
  height: 400px;
  top: 0;
  left: 0;
  margin: auto;
  right: 0;
  bottom: 0;
  top: -338px;
}
.login .login-title{
  width: 100%;
  text-align: center;
}
.login-title img{
  width: 190px;
  height: auto;
}
.login-title p{
  font-family: PingFangSC-Regular;
  font-size: 18px;
  color: #fff;
  letter-spacing: .29px;
  padding-top: 10px;
  padding-bottom: 50px;
}
.login_box{
  width: 400px;
  height: auto;
  background: #fff;
  box-shadow: 0 2px 4px 0 rgba(0,0,0,.5);
  border-radius: 4px;
  margin: 0 auto;
  padding-bottom: 40px;
}
.login_box .title{
  font-size: 20px;
  color: #9b9b9b;
  letter-spacing: .32px;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  justify-content: space-around;
  padding: 50px 60px 0 60px;
  margin-bottom: 20px;
  cursor: pointer;
}
.login_box .title span:nth-of-type(1){
  color: #4a4a4a;
  border-bottom: 2px solid #84cc39;
}

.inp{
  width: 350px;
  margin: 0 auto;
}
.inp input{
  border: 0;
  outline: 0;
  width: 100%;
  height: 45px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  text-indent: 20px;
  font-size: 14px;
  background: #fff !important;
}
.inp input.user{
  margin-bottom: 16px;
}
.inp .rember{
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  margin-top: 10px;
}
.inp .rember p:first-of-type{
  font-size: 12px;
  color: #4a4a4a;
  letter-spacing: .19px;
  margin-left: 22px;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
  /*position: relative;*/
}
.inp .rember p:nth-of-type(2){
  font-size: 14px;
  color: #9b9b9b;
  letter-spacing: .19px;
  cursor: pointer;
}

.inp .rember input{
  outline: 0;
  width: 30px;
  height: 45px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  text-indent: 20px;
  font-size: 14px;
  background: #fff !important;
}

.inp .rember p span{
  display: inline-block;
  font-size: 12px;
  width: 100px;
  /*position: absolute;*/
  /*left: 20px;*/

}
#geetest{
  margin-top: 20px;
}
.login_btn{
  width: 100%;
  height: 45px;
  background: #84cc39;
  border-radius: 5px;
  font-size: 16px;
  color: #fff;
  letter-spacing: .26px;
  margin-top: 30px;
}
.inp .go_login{
  text-align: center;
  font-size: 14px;
  color: #9b9b9b;
  letter-spacing: .26px;
  padding-top: 20px;
}
.inp .go_login span{
  color: #84cc39;
  cursor: pointer;
}
</style>
