import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
const GoodsList=()=>import("@/views/Goods/GoodsList/GoodsList.vue")
const Detail=()=>import("@/views/Goods/Goods/Detail.vue")
const Login=()=>import("@/views/Login/Login.vue")
const Register=()=>import("@/views/Login/Register.vue")
const Reset=()=>import("@/views/Login/Reset.vue")
const Cart=()=>import("@/views/Cart/Cart.vue")
const Order=()=>import("@/views/Order/Order.vue")
const Profile=()=>import("@/views/Profile/Profile.vue")
const OrderPay=()=>import("@/views/Order/OrderPay.vue")

const routes = [
    {
        path:'/',
        name:'home',
        component:HomeView,
        meta:{
            title: '商城首页'
        }
    },
    {
        path:'/goods_list/:keyword/:page/:order',
        name:'GoodsList',
        component:GoodsList,
        meta:{
            title: '商品列表页'
        }
    },
    {
        path:'/detail/:sku_id',
        name:'Detail',
        component:Detail,
        meta:{
            title: '商品详情页',
            isAuthRequired: true
        }
    },

    {
        path:'/login',
        name:'Login',
        component:Login,
        meta:{
            title: '欢迎登录'
        }
    },
    {
        path:'/register',
        name:'Register',
        component:Register,
        meta:{
            title: '欢迎注册'
        }
    },
    {
        path:'/reset',
        name:'Reset',
        component:Reset,
        meta:{
            title: '忘记密码'
        }
    },
    {
        path:'/cart/detail',
        name:'Cart',
        component:Cart,
        meta:{
            title: '购物车',
            isAuthRequired: true
        }
    },
    {
        path:'/Order/:trade_no',
        name:'Order',
        component:Order,
        meta:{
            title: '订单页面',
            isAuthRequired: true
        }
    },
    {
        path:'/Order/Pay',
        name:'OrderPay',
        component:OrderPay,
        meta:{
            title: '收银台',
            isAuthRequired: true
        }
    },
        {
        path:'/profile',
        name:'Profile',
        component:Profile,
        meta:{
            title: '个人主页',
            isAuthRequired: true
        }
    },
]



const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

import store from '../store'
    // 导航守卫拦截前端
    // 拦截器给后端看
router.beforeEach((to, from, next) => {
    document.title = to.meta.title
    if (to.meta.isAuthRequired==true && store.state.user.isLogin==false) {
        next('/login')
    }else {
        next() // 必须调用 next() 继续导航
    }

})


export default router
