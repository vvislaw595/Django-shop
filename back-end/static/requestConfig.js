import axios from 'axios';

export function request(config){
    const instance = axios.create({
        baseURL:'http://localhost:8000',
        timeout:5000,
    })

    // 拦截请求
    instance.interceptors.request.use(config=>{
        // 一般来讲这里写实例+token

        // 直接放行
        return config;
    },error=>{
        // 这里写错误代码
    })

    // 响应拦截
    instance.interceptors.response.use(res=>{
        return res.data?res.data:res;
    },error=>{
        // 处理错误响应，如404 500

    })
    
    return instance(config);
}