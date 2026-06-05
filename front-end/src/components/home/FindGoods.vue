<template>
  <div class="find-goods">
    <img src="@/assets/images/find-goods.png" alt="">
    <div class="scroll-container">
      <vue3ScrollSeamless
        :classOptions="classOptions"
        :dataList="goodsList">

        <div class="scroll-wrapper">
          <div class="item" v-for="(item, index) in goodsList"
               :key="index"
               @click="toGoodsDetail(item.sku_id)">

            <div v-if="index % 2 === 0">
              <span class="dian1">{{item.name}}</span>
              <img :src="item.image" alt="">
            </div>

            <div v-else>
              <img :src="item.image" alt="">
              <span class="dian1">{{item.name}}</span>
            </div>

          </div>
        </div>
      </vue3ScrollSeamless>
    </div>
  </div>
</template>

<script setup>
import {getFindGoods} from "@/network/home.js"
import {onMounted, ref} from "vue";
import {toGoodsDetail} from "@/utils/goods.js";

const goodsList = ref([])

const classOptions = {
  limitMoveNum: 5,
  // 个人是喜欢向右滚动的
  direction: 3,   // 向右
                  // 但是向右滚动，一开始渲染出来的0-4 五个item
                  // 如果 滚动条不滚，是可以正常点击转跳
                  // 一旦 滚动条开始滚了，就要等到index15的item出来才能点
  // 向左滚是没问题的
  // direction: 2,   // 向左滚动可以保证每个item都可以正常点击转跳页面

  step: 0.8,
  hoverStop: true,
};

onMounted(() => {
  getFindGoods().then(res => {
    // console.log(res.data)
    goodsList.value = res.data
  })
})
</script>

<style scoped lang="less">
.find-goods{
  width: var(--content-width);
  margin: 0 auto;
  >img{
    width: 190px;
    height: 260px;
    float: left;
  }
  .scroll-container {
    height: 260px;
    width: 990px;
    overflow: hidden;
    margin-left: 210px;
    background-color: #fff;
    display: flex;
  }

  .scroll-wrapper {
    display: flex;
    flex-wrap: nowrap;
  }

  .item {
    flex-shrink: 0; // 防止项目被压缩
    &:hover{
      cursor: pointer;
      display: flow;
    }
    height: 260px;
    width: 150px;
    margin-top: 15px;
    padding: 10px;
    span{
      width: 150px;
      font-size: 15px;
      margin: 10px 10px;
    }
    img {
      padding: 10px;
      width: 150px;
      height: 150px;
      border-radius: 20px;
    }
  }
}
</style>