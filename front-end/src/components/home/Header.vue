Header原稿
Header_test 新增了上方Header的粘性布局


<template>
  <div class="main clearfix">
    <div class="content ">
      <div class="logo fl">
        <Logo></Logo>
      </div>
      <div class="search-box fl ">
        <div class="search-input fl">
          <SearchBox></SearchBox>
        </div>
        <div class="shopcart fl">
          <ShopCart></ShopCart>
        </div>
      </div>
      <div class="right fr">
        <img src="@/assets/images/header-right.png" alt="">
      </div>
    </div>
  </div>
</template>

<script setup>
import Logo from "@/components/common/Logo.vue";
import SearchBox from "@/components/home/SearchBox.vue";
import ShopCart from "@/components/home/ShopCart.vue";
import Header_test from "@/components/home/Header_test.vue";
</script>

<style scoped lang="less">
.main {
  .content {
    width: var(--content-width);
    margin: 0 auto;
    height: 140px;
    //border: 1px solid red;
  }
    .logo{
        margin-left: 60px;
        //border: 1px solid red;
    }

  .search-box {
    width: 800px;
    height: 70px;
    margin-left: 50px;
      //border: 1px solid red;
  }
    .shopcart{
        margin-left: 5px;
        //border: 1px solid red;
    }

  .right {
    img {
      width: 180px;
        //border: 1px solid red;
    }

    line-height: 140px;
  }
}
</style>