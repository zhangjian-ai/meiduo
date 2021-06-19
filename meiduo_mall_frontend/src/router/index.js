import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import BindUser from '../views/BindUser.vue'
import UserCenter from '../views/UserCenter.vue'
import Detail from '../components/Detail.vue'
import VerifyEmail from '../components/VerifyEmail.vue'
import VerifyOrder from '../components/VerifyOrder.vue'
import Address from '../components/Address.vue'
import Orders from '../components/Orders.vue'
import Skus from '../views/Skus.vue'
import SkuDetail from '../views/SkuDetail.vue'
import Cart from '../views/Cart.vue'
import CreateOrder from '../views/CreateOrder.vue'
import GoodsList from '../views/GoodsList.vue'




Vue.use(VueRouter)

// 解决ElementUI导航栏中的vue-router在3.0版本以上重复点菜单报错问题，跳转当前路由报错
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

const originalReplace = VueRouter.prototype.replace;
VueRouter.prototype.replace = function replace(location) {
  return originalReplace.call(this, location).catch(err => err);
}

const routes = [
  {
    path: '/register',
    name: 'register',
    component: Register,
    meta: {
      title: '注册',
    }
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: {
      title: '登陆',
    }
  },
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: {
      title: '首页',
    }
  },
  {
    path: '/skus',
    name: 'skus',
    component: Skus,
    meta: {
      title: '购物广场',
    }
  },
  {
    path: '/goods_list',
    name: 'goods_list',
    component: GoodsList,
    meta: {
      title: '搜索商品',
    }
  },
  {
    path: '/sku_detail',
    name: 'sku_detail',
    component: SkuDetail,
    meta: {
      title: '商品详情',
    }
  },
  {
    path: '/cart',
    name: 'cart',
    component: Cart,
    meta: {
      title: '购物车',
    }
  },
  {
    path: '/oauth_callback.html',
    name: 'binduser',
    component: BindUser,
    meta: {
      title: '用户绑定',
    }
  },
  {
    path: '/verify_order',
    name: 'verify_order',
    component: VerifyOrder,
    meta: {
      title: '支付信息',
    }
  },
  {
    path: '/create_order',
    name: 'create_order',
    component: CreateOrder,
    meta: {
      title: '确认订单',
      requireAuth: true
    }
  },
  {
    path: '/user_center',
    name: 'user_center',
    component: UserCenter,
    children: [
      {
        path: 'detail', //以“/”开头的嵌套路径会被当作根路径，所以子路由上不用加“/”;在生成路由时，主路由上的path会被自动添加到子路由之前，所以子路由上的path不用在重新声明主路由上的path了。
        name: 'detail',
        component: Detail,
        meta: {
          title: '用户中心',
          requireAuth: true
        }
      },
      {
        path: 'address',
        name: 'address',
        component: Address,
        meta: {
          title: '收货地址',
          requireAuth: true
        }
      },
      {
        path: 'orders',
        name: 'orders',
        component: Orders,
        meta: {
          title: '我的订单',
          requireAuth: true
        }
      },
      {
        path: 'verify_email',
        name: 'verify_email',
        component: VerifyEmail,
      },
    ]

  },
  // {
  //   path: '/about',
  //   name: 'About',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  // }
]

const router = new VueRouter({
  mode: 'history', //取出域名后面的# 
  routes
})



export default router
