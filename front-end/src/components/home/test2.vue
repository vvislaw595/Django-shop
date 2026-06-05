用于测试 FindGoods 滚动条
废稿


<template>
  <div class="find-goods">
    <img src="@/assets/images/find-goods.png" alt="">
    <div class="scroll-container">
      <vue3ScrollSeamless
        :classOptions="classOptions"
        :dataList="goodsList">

        <div class="scroll-wrapper">
          <div class="item" v-for="(item, index) in goodsList" :key="index">

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
import FindGoods from "@/components/home/FindGoods.vue";

const goodsList = ref([])

const classOptions = {
  limitMoveNum: 5,
  direction: 3,   // 向右
  step: 0.5,
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
    width: 1000px;
    overflow: hidden;
    margin-left: 220px;
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