// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import settings from './settings'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios'

axios.defaults.withCredentials = false;
Vue.config.productionTip = false
Vue.prototype.$settings = settings
Vue.prototype.$axios= axios
/* eslint-disable no-new */
Vue.use(ElementUI);

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
