import {request} from "@/network/requestConfig.js";

export function getCartDetailData(){
    return request({
        url: "cart/detail/",
        method:"post"
    })
}

export function updateCartGoodsNumData(data){
    return request({
        url: "/cart/num/",
        method:"post",
        data
    })
}

export function addCart(data){
    return request({
        url: "/cart/",
        method:"post",
        data
    })
}

export function getCartcount(){
    return request({
        url: "/cart/count/",
        method:"post",
    })
}

export function deleteCartGoods(data){
    return request({
        url: "/cart/delete/",
        method:"post",
        data
    })
}