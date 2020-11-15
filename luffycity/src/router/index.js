import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login'
import Register from '@/components/Register'
import Course from '@/components/Course'
import Detail from '@/components/Detail'
import Cart from "@/components/Cart"
import Order from "@/components/Order"
import Success from "@/components/Success"
import Myorder from '@/components/Myorder'
import Player from '@/components/Player'

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
    },
    {
      path: '/user/register',
      component: Register,
    },
    {
      path: '/Course',
      component: Course,
    },
    {
      path: '/course/detail/:id/',
      component: Detail
    },
    {
      path: '/cart',
      name: 'Cart',
      component: Cart
    },
    {
      path: '/order',
      name: 'Order',
      component: Order
    },
    {
      path: '/payments/result/',
      name: 'Success',
      component: Success
    },
    {
      path: '/myorder/',
      component: Myorder
    },
    {
      path: '/polyv/player/:vid',   // /course/detail/1/   this.$route.params.vid
      component: Player
    },
  ]
})
