<template>
  <div>
    <Shortcut></Shortcut>
    <Header_test></Header_test>
    <div class="goods">
      <div class="good clearfix">
<!--        {{goodsList}}-->
        <div class="fl">
          <img :src="goodsList.data.image" alt="">
        </div>
        <div class="good-content fl">
          <div class="desc">{{goodsList.data.name}}</div>
          <div class="price">{{goodsList.data.p_price}}</div>
          <div class="count">
              <el-input-number
                v-model="num"
                @change="handleChange"
                :min="1"
                :max="10"
                size="large"
                label=""></el-input-number>
          </div>
          <a href="#"
             class="add_cart"
             @click="addCartData(goodsList.data.sku_id,num,0)">加入购物车</a>
        </div>
      </div>
      <div class="comment">
        <Comment :skuId="$route.params.sku_id"></Comment>
      </div>
    </div>
  </div>
</template>

<script setup>
import Shortcut from "@/components/common/Shortcut.vue";
import Header_test from "@/components/home/Header_test.vue";
import Comment from "@/components/goodsDetail/Comment.vue";

import {addCartData} from "@/utils/goods.js"
import {getGoodsDetail} from "@/network/goods.js"
import {onMounted, reactive, ref} from "vue";
import {useRoute} from "vue-router";



const route = useRoute();
let skuId = ref("");
let goodsList = reactive({
  data:{}
});

onMounted(() => {
  skuId.value = route.params.sku_id;
  getGoodsDetail(skuId.value).then(res => {
    goodsList.data = res.data;
  })
})

let num = ref(1)
const handleChange=(value)=>{
  num.value = value;
}


</script>

<style scoped lang="less">
.goods{
    width: var(--content-width);
    margin: 0 auto;
  .good{
    img{
      width: 350px;
      height: 350px;
    }
    .good-content{
      margin-top: 70px;
      margin-left: 40px;
      width: 600px;
      .desc{
        font-size: 16px;
        color: #666666;
      }
      .price{
        margin-top: 10px;
        font-size: 22px;
        color: #e4393c;
      }
      .count{
        margin-top: 10px;
      }
      .add_cart{
        margin-top: 10px;
        display: block;
        width: 180px;
        height: 50px;
        background-color: red;
        color: #fff;
        font-size: 18px;
        font-weight: 700;
        text-align: center;
        line-height: 50px;
      }
    }
  }
  .comment{
    margin-top: 20px;
  }
}
</style>