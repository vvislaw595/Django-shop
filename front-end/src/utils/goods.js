import {addCart} from "@/network/cart.js";
import store from "@/store/index.js";



export function toGoodsDetail(skuId){
    window.open("/detail/"+skuId);
}

// 添加商品进去购物车
export function addCartData(skuId,nums,isDelete=0){
    let requestData = {
        sku_id:skuId,
        nums:nums,
        is_delete:isDelete,
    }
    addCart(requestData).then((res)=>{
        if (res.status == 200){
            alert(res.data);         // data合不合适 要在后端修改
        }
        else {
            alert(res.data);
        }
        store.dispatch("updateCart");   // 去到store的actions里面
    });
}

