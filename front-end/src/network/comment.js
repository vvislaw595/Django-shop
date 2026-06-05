import {request} from "@/network/requestConfig.js";

export function getCommentCountData(skuId){
    return request({
        url: "/comment/count?sku_id="+skuId,
    })
}

export function getCommentDetailData(skuId,page){
    return request({
        url: "/comment/detail?sku_id="+skuId+"&page="+page,
    })
}