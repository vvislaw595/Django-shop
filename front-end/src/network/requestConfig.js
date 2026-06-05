import axios from 'axios';
import store from "@/store";


export function request(config){
    const instance = axios.create({
        baseURL:'/api',
        timeout:5000,
        withCredentials: true,
    })

    // 拦截请求
    // 导航守卫拦截前端
    // 拦截器给后端看
    instance.interceptors.request.use(config=>{
        // 一般来讲这里写实例+token
        const token = window.localStorage.getItem("token");
        if(token){
            config.headers.Authorization = token;
        }

        // 直接放行
        return config;
    },err=>{
        // 这里写错误代码
    })

    // 响应拦截
    instance.interceptors.response.use(res=>{
        if(res.data.status == false){
            window.localStorage.setItem("token","");
            store.commit("setLogin",false)
        }

        return res.data?res.data:res;
    },err=>{
        // 处理错误响应，如404 500

    })

    return instance(config);
}