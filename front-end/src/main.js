import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import "@/assets/css/config.css"
//iconfont
import "@/assets/iconfont/iconfont.css"
// ElementPlus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 滚动插件
import vue3SeamlessScroll from "vue3-seamless-scroll";
import {vue3ScrollSeamless} from "vue3-scroll-seamless";

createApp(App)
    .use(router)
    .use(store)
    .use(ElementPlus)
    .use(vue3SeamlessScroll)
    .component('vue3ScrollSeamless',vue3ScrollSeamless)
    .mount('#app')

