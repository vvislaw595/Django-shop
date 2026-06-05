<template>
  <div>

    <Shortcut></Shortcut>
    <Header_test></Header_test>
    <div class="inner">
          <Navigation></Navigation>
      <div class="find-goods">
        <FindGoods></FindGoods>
      </div>
      <div class="category clearfix">
        <div @click="toCategory(item.typeId)" class="content fl" v-for="(item,index) in category" :key="index">
          <div >
              <div class="category-title" :class="{selected_title: item.selected}">{{item.title}}</div>
              <div class="category-content" :class="{selected_content: item.selected}">{{item.content}}</div>
          </div>

        </div>
      </div>
      <Category :categoryId="categoryId"></Category>
    </div>


    <div>
<!--        <el-backtop right="80" bottom="200"></el-backtop>-->
        <BackTop></BackTop>
      我是个主页
    </div>
  </div>

</template>

<script setup>
import {ref} from "vue";

import Shortcut from "@/components/common/Shortcut.vue";
import Header from "@/components/home/Header.vue";
import Navigation from "@/components/home/Navigation.vue";
import FindGoods from "@/components/home/FindGoods.vue";
import Category from "@/components/home/Category.vue";
import Header_test from "@/components/home/Header_test.vue";
import BackTop from "@/components/common/BackTop.vue";



// import test2 from "@/components/home/test2.vue"


let category = ref([
    {typeId:1,title:"精选",content:"猜你喜欢",selected:true},
    {typeId:2,title:"智能先锋",content:"大电器城",selected:false},
    {typeId:3,title:"优品家具",content:"品质生活",selected:false},
    {typeId:4,title:"超市百货",content:"生鲜百货",selected:false},
    {typeId:5,title:"时尚潮流",content:"美妆穿搭",selected:false},
    {typeId:6,title:"进口好物",content:"国际商品",selected:false},
])
let categoryId = ref(1);
const toCategory=(typeId)=>{
  categoryId.value=typeId;
  for(let i in category.value){
    category.value[i].selected=false;
    if(typeId == (parseInt(i)+1)){
      category.value[i].selected=true;
    }
  }
}
</script>

<style scoped lang="less">
.inner {
  background-color: #F5F6FA;
  .find-goods {
    padding-top: 15px;
    padding-bottom: 15px;
  }
  .category{
    width:var(--content-width);
    //margin-left: 132px;       // 这样才能让他在中间
    // 但是只是相对定位在中间
    margin: 0 auto;
    background-color: #fff;
    height: 70px;
    text-align: center;
    .content{
      margin-top: 10px;
      width: 198px;       // 200撑满 过大会换行，而且现在不能对齐
      &:not(:last-child){
        border-right: 2px solid #e8e8e8;
      }
      .category-title{
        font-size: 16px;
        font-weight: 700;
        height: 30px;
        line-height: 30px;
      }
      .category-content{
        font-size: 14px;
        color: gray;      // 权重大
      }
      &:hover{
        cursor:pointer;
        color: #e1251b;
      }
      &:hover div:last-child{  // 上下两个文字都有效果
        cursor:pointer;
        color: #e1251b;
      }
      >div{
        width: 80px;

        margin: 0 auto;
      }
      .selected_title{
        background-color: #e1251b;
        color: #fff;
        border-radius: 15px;
      }
      .selected_content{
        color: #e1251b;
      }
    }
  }
}
</style>
