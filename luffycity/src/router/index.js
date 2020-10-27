import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'

Vue.use(Router)

export default new Router({
  mode:'history',
  routes: [
    {
      path: '/',
      // name: 'HelloWorld',
      component: Home
    },
        {
      path: '/home',
      // name: 'HelloWorld',
      component: Home
    }
  ]
})
