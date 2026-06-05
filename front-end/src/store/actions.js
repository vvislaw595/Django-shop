// 加入
import {getCartcount} from "@/network/cart.js";


const actions = {
    updateCart({commit,state}) {
        getCartcount().then(res => {
            let count = 0;
            console.log(res.data);      // nums__sum
            if(res.data.nums__sum>0){
                count = res.data.nums__sum;

            }
// 不知道要不要else，如果要，直接等于0
            window.localStorage.setItem("count", count.toString());
            commit("updateCartCount", {count: count});
            // return count;
        })
    }
}

export default actions;