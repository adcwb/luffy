import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login'

Vue.use(Router)

export default new Router({
  mode:'history',
  routes: [
    {
      path: '/',
      // name: 'HelloWorld',
      component: Home,
    },
    {
      path: '/home',
      // name: 'HelloWorld',
      component: Home,
    },
    {
      path: '/user/login',
      component: Login,
    }
  ]
})
