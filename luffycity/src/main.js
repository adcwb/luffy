// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import settings from "./settings";

Vue.config.productionTip = false
Vue.prototype.$settings = settings;  //将settings中的内容作为vue的属性，以后就不用每次都导包了
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
