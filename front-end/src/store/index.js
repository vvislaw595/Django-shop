import {createStore} from 'vuex'
import mutations from './mutations.js'
import actions from './actions.js'
// 从本地获取

const state = {
    user:{
        isLogin:window.localStorage.getItem("token")?true:false,
        name:window.localStorage.getItem("username")?window.localStorage.getItem("username"):"",
        is_superuser: window.localStorage.getItem("is_superuser") === "true" ? true : false,
    },
    cartCount:window.localStorage.getItem("count") || 0,
}

export default createStore({
    state,
    getters: {},
    mutations,
    actions,
    modules: {},

})