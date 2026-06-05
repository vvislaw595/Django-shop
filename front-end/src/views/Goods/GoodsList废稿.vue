<template>
  <div>
    <Shortcut></Shortcut>
    <Header_test></Header_test>

    <div class="all-goods">
      <div>
        <span>全部商品分类</span>
      </div>
    </div>
    <div class="all-goods-list">
      <div class="result-keyword">
        <span class="all-result-font">
          全部结果&nbsp;&nbsp;>&nbsp;&nbsp;
        </span>

        <span class="search-word">
          "{{keyword}}"
        </span>
      </div>
      <div class="goods-list">
        <div class="search-condition">
          <a href="#" v-for="(item,index) in orderTypes"
             :key="index"
             @click="changeOrder(item.order,item.index)"
             :class="item.isActive?'current-condition':'not-current-condition'">
            <span>{{item.name}}</span>
            <img src="" alt="">
          </a>
        </div>
        <div class="list-detail clearfix">
          <div class="every-goods fl" v-for="(item,index) in goodsListData" :key="index">
            <div>
              <img :src="item.image" class="goods_image" alt="">
            </div>
            <div class="price">
              ￥{{item.p_price}}
            </div>
            <div class="name cs dian2">
              {{item.name}}
            </div>
            <div class="comment_count">
              <span class="count">{{item.comment_count?item.comment_count:0}}</span>
              <span class="comment">条评价</span>
            </div>
            <div class="shop_name">
              {{item.shop_name}}
            </div>
            <div class="add_cart cs">
              <img src="../../assets/images/cart/add-cart1.png" alt="">加入购物车
            </div>
          </div>
<!--          {{goodsListData}}-->
        </div>
      </div>

      <div class="change_page">
        <el-pagination background
                       layout="prev, pager, next"
                       :total="goodsCount"
                       :page-size="15"
                       :current-page="parseInt(route.params.page) || 1"
                       @current-change="handleCurrentChange"
                       class="custom-pagination"/>
      </div>
    </div>
  </div>
</template>




<script setup>
import Shortcut from "@/components/common/Shortcut.vue";
import Header_test from "@/components/home/Header_test.vue";
import {computed, onMounted, ref, watch} from "vue";
import {useRouter,useRoute} from "vue-router";
import {getGoodsListData, getKeywordGoodsCountData} from "@/network/goods.js";

const router = useRouter();   // 全局的
const route = useRoute();     // 当前的

let orderTypes = ref([
  // index哪个是活动的，order按什么排序
  // comment from goods.views :
  //                          order  # 1按评论数排序，2按价格排序
  {index:1,order:1,name:"综合",isActive:true},
  {index:2,order:1,name:"评论数",isActive:false},
  {index:3,order:2,name:"价格",isActive:false},
]);

let goodsListData = ref([])

const getSearchData = (keyword,page,order)=>{
  getGoodsListData(keyword,page,order).then(res=>{
    // console.log(res.data)
    goodsListData.value = [];
    for(let i in res.data){
      goodsListData.value.push(JSON.parse(res.data[i]));
    }
  })
}

let goodsCount = ref(0);

const getKeywoordGoodsCount=(keyword)=>{
  getKeywordGoodsCountData(keyword).then(res=>{
    goodsCount.value = res;
  })
}

  // 页面加载后的动作
  onMounted(()=>{
    getSearchData(route.params.keyword,
                  route.params.page,
                  route.params.order);
    getKeywoordGoodsCount(route.params.keyword);
  })
// 定义三个变量，监听
let keyword = computed(()=>{
  return route.params.keyword;
})

let page = computed(()=>{
  return route.params.page;
})

let order = computed(()=>{
  return route.params.order;
})

watch(keyword,(newValue,oldValue)=>{
  getSearchData(newValue,1,1);
  getKeywoordGoodsCount(newValue);
})

watch(page,(newValue,oldValue)=>{
  getSearchData(keyword.value,newValue,1);
})

watch(order,(newValue,oldValue)=>{
  getSearchData(keyword.value,1,newValue);
})



const changeOrder = (currentOrder,index) => {
  // 这里用全局刷新
  // 也可以像category一样用局部刷新
  router.push("/goods_list/"+route.params.keyword+"/"+1+"/"+currentOrder)


  // 点击后的样式变换
  for(let i in orderTypes.value) {
    if(orderTypes.value[i].index==index){
      orderTypes.value[i].isActive=true;
    }
    else {
      orderTypes.value[i].isActive=false;
    }
  }
}


const handleCurrentChange=(val)=>{
  // console.log(val)
  router.push("/goods_list/"+keyword.value+"/"+val+"/"+order.value);
}

</script>




<style scoped lang="less">
  .all-goods{
    border-bottom: 2px solid red;
    div{
        width: var(--content-width);
        margin: 0 auto;
      span{
        display: block;

        background-color: red;
        color: white;
        font-size: 14px;
        height: 33px;
        width: 190px;
        line-height: 33px;
        text-align: center;
      }
    }
  }
  .all-goods-list{
    width: var(--content-width);
    margin: 0 auto;
    .result-keyword{
      margin-top: 20px;
      .all-result-font{
        color: #666;
        font-size: 14px;
      }
      .search-word{
        color: #666;
        font-weight: 700;
        font-size: 14px;
      }
    }
    .search-condition{
      margin-top: 10px;
      background-color: #f1f1f1;
      height: 40px;
      line-height: 40px;

      .current-condition{
        background-color: #e4393c;
        border: 2px solid #e4393c;
        color: #fff;
        img{
          content:url("@/assets/images/goods-list/down3.png")
        }
      }
      .not-current-condition{
        background-color: #fff;
        border: 2px solid #dddddd;
        img{
          content:url("@/assets/images/goods-list/down1.png")
        }
        &:hover{
          border: 2px solid #e4393c;
          img{
          content:url("@/assets/images/goods-list/down2.png")

          }
        }
      }
      a{
        display: inline-block;
        text-align: center;
        height: 25px;
        line-height: 25px;
        width: 80px;
        font-size: 14px;

        img{
          width: 14px;
          height: 14px;
          margin-left: 5px;
        }
        &:first-child{
          margin-left: 10px;
        }
      }
    }
    .list-detail{
      .every-goods{
        margin-top: 10px;
        border: 1px solid #fff;
        width: 238px;
        height: 420px;
        &:hover{
          border: 1px solid #e3e4e5;
        }
        .goods_image{
          margin-top: 10px;
          width: 220px;
          height: 220px;
        }
        .price{
          margin-top: 10px;
          margin-left: 5px;
          color: #F30213;
          font-size: 20px;
        }
        .name{
          margin-top: 10px;
          font-size: 14px;
          color: #666;
          margin-left: 5px;
          &:hover{
            color: #e4393c;
          }
        }
        .comment_count{
          margin-left: 5px;
          margin-top: 10px;
          .count{
            color: #646fb0;
            font-weight: 700;
          }
          .comment{
            color: #a7a7a7;
            font-size: 13px;
          }
        }
        .shop_name{
          margin-left: 5px;
          margin-top: 10px;
          color: #999;
        }
        .add_cart {
          margin-top: 10px;
          border: 1px solid #e4393c;
          text-align: center;
          img{
            width: 20px;
          }
          &:hover{
            color: #e4393c;
          }
        }
      }
    }

    .change_page{
      margin-top: 50px;
      margin-bottom: 100px;
      margin-left: 45%;
      --el-color-primary: red;
    }
  }
</style>