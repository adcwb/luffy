export default {
  Host:"http://api.adcwb.com",
  check_login(ths){
    let token = localStorage.token || sessionStorage.token;

    if (token){

        ths.$axios.post(`${this.Host}/users/verify/`,{
            token:token,
          }).then((res)=>{

            ths.token = token;
          }).catch((error)=>{
            ths.token = false;
            sessionStorage.removeItem('token');
            sessionStorage.removeItem('username');
            sessionStorage.removeItem('id');
            localStorage.removeItem('token');
            localStorage.removeItem('username');
            localStorage.removeItem('id');
          })


      } else {
        ths.token = false
      }

  }
}
