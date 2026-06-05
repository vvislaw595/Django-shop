import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'

const routers = [
    {
        path:'/',
        name:'home',
        component:HomeView,
        meta:{
            title: '商城首页'
        }
    },

]

const router = createRouter({
    history:createWebHistory(process.env.BASE_URL),
    routers
})

router.beforeEach((to,from) => {
    document.title = to.meta.title;
})


export default router
