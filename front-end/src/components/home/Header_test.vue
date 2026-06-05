<template>
  <div class="main clearfix" :class="{ 'scrolled': isScrolled }">
    <div class="content">
      <div class="logo fl">
        <Logo></Logo>
      </div>
      <div class="search-box fl">
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
import { ref, onMounted, onUnmounted } from 'vue';
import SearchBox from "@/components/home/SearchBox.vue";
import Logo from "@/components/common/Logo.vue";
import ShopCart from "@/components/home/ShopCart.vue";

const isScrolled = ref(false);

const handleScroll = () => {
  isScrolled.value = window.scrollY > 0; //这样就不抽了
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped lang="less">
.main {
  position: sticky;
  top: 0;
  z-index: 1000;
	width: 100%;
  background-color: white;

    //      把动画效果都注释了
    // 滚第一下     不知道为什么会抽搐

  //transition: all 0.3s ease;

  .content {
    width: var(--content-width);
    margin: 0 auto;
    height: 140px;

    //transition: all 0.3s ease;
  }

  .logo {
    margin-left: 60px;

    //transition: all 0.3s ease;
  }

  .search-box {
    width: 800px;
    height: 70px;
    margin-left: 50px;

    //transition: all 0.3s ease;
  }

  .shopcart {
    margin-left: 5px;

    //transition: all 0.3s ease;
  }

  .right {
    img {
      width: 180px;

      //transition: all 0.3s ease;
    }

    line-height: 140px;
    //transition: all 0.3s ease;
  }

  // 滚动后
  &.scrolled {

    .content {
      height: 80px;
      display: flex;
      align-items: center;
    }

    .logo {
      margin-left: 40px;
      transform: scale(0.75);
    }

    .search-box {
      margin-left: 115px;
      transform: scale(0.9);
      height: 50px;
      margin-bottom: 95px;
    }

    .shopcart {
      transform: scale(0.9);
    }

    .right {
      line-height: 80px;

      img {
        width: 130px;
          height: 80px;
      }
    }
  }
}
</style>