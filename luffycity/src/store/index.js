import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  // 数据仓库,类似vue组件里面的data
  state: {
    cart_length: 0,  // 购物车数据
  },

  // 数据操作方法,类似vue里面的methods
  mutations: {    // 修改购物车的商品总数
    add_cart (state, cart_length) {
      state.cart_length = cart_length;
    }
  }

})

