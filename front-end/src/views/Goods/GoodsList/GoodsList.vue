<template>
  <div>
    <Shortcut></Shortcut>
    <Header_test></Header_test>
	  <back-top></back-top>
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
          <a href="javascript:" v-for="(item,index) in orderTypes"
             :key="index"
             @click="changeOrder(item.order,item.index)"
             :class="item.isActive?'current-condition':'not-current-condition'">
            <span>{{item.name}}</span>
            <img src="" alt="">
          </a>
        </div>
        <div class="list-detail clearfix">
          <div class="every-goods fl"
               v-for="(item,index) in goodsListData"
               :key="index">
            <div >
              <img :src="item.image"
                   @click="toGoodsDetail(item.sku_id)"
                   class="goods_image" alt="">
            </div>
            <div class="price">
              ￥{{item.p_price}}
            </div>
            <div class="name cs dian2"
                 @click="toGoodsDetail(item.sku_id)">
              {{item.name}}
            </div>
            <div class="comment_count">
              <span class="count">{{item.comment_count?item.comment_count:0}}</span>
              <span class="comment">条评价</span>
            </div>
            <div class="shop_name">
              {{item.shop_name}}
            </div>
            <div class="add_cart cs" @click="addCartData(item.sku_id,1,0)">
              <img src="@/assets/images/cart/add-cart1.png" alt="">加入购物车
            </div>
          </div>
        </div>
      </div>

      <div class="change_page">
        <el-pagination background
                       layout="prev, pager, next"
                       :total="goodsCount"
                       :page-size="15"
                       :current-page="currentPage"
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
import {useRoute} from "vue-router";
import {getGoodsListData, getKeywordGoodsCountData} from "@/network/goods.js";
import {addCartData, toGoodsDetail} from "@/utils/goods.js";
import BackTop from "@/components/common/BackTop.vue";


const route = useRoute();

let currentPage = ref(1);
let currentOrder = ref(1); // API排序参数
let currentOrderIndex = ref(1); // UI激活状态索引
let keyword = ref("");

let orderTypes = ref([
  {index:1, order:1, name:"综合", isActive:true},
  {index:2, order:3, name:"评论数", isActive:false},
  {index:3, order:2, name:"价格", isActive:false},
]);

let goodsListData = ref([]);
let goodsCount = ref(0);

// 获取数据
const getSearchData = async () => {
  try {
    const res = await getGoodsListData(keyword.value, currentPage.value, currentOrder.value);
    goodsListData.value = [];
    for(let i in res.data){
      goodsListData.value.push(JSON.parse(res.data[i]));
    }
  } catch (error) {
    console.error("获取商品数据失败:", error);
  }
};

const getKeywordGoodsCount = async () => {
  try {
    const res = await getKeywordGoodsCountData(keyword.value);
    goodsCount.value = res;
  } catch (error) {
    console.error("获取商品数量失败:", error);
  }
};

// 初始化数据
const initData = async () => {
  keyword.value = route.params.keyword;
  currentPage.value = parseInt(route.params.page) || 1;
  currentOrder.value = parseInt(route.params.order) || 1;

  // 根据order值设置初始激活状态
  if (currentOrder.value === 1) {
    currentOrderIndex.value = 1; // 默认激活"综合"
  } else if (currentOrder.value === 2) {
    currentOrderIndex.value = 3; // 激活"价格"
  }

  await Promise.all([
    getSearchData(),
    getKeywordGoodsCount()
  ]);

  updateActiveOrderType();
};

// 更新排序按钮激活状态
const updateActiveOrderType = () => {
  orderTypes.value.forEach(item => {
    item.isActive = item.index === currentOrderIndex.value;
  });
};

// 页面加载
onMounted(() => {
  initData();
});

// 排序切换
const changeOrder = (order, index) => {
  currentOrder.value = order;
  currentOrderIndex.value = index;
  currentPage.value = 1; // 排序切换时回到第一页

  updateActiveOrderType();
  getSearchData();
};

// 分页切换
const handleCurrentChange = (page) => {
  currentPage.value = page;
  getSearchData();
		window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
};

// 监听路由关键词变化（用于处理从其他页面跳转过来的情况）
watch(
  () => route.params.keyword,
  (newKeyword) => {
    if (newKeyword && newKeyword !== keyword.value) {
      keyword.value = newKeyword;
      currentPage.value = 1;
      currentOrder.value = 1;
      currentOrderIndex.value = 1;

      initData();
    }
  }
);
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
	        //cursor: pointer;
	        opacity: 0.75;
        }
        .goods_image{
          margin-top: 10px;
          width: 220px;
          height: 220px;
	        cursor: pointer;
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