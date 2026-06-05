<template>
  <div class="nav ">
    <div class="main clearfix">
      <div class="menu fl">
        <LeftMenu></LeftMenu>
      </div>
      <div class="banner">
        <Banner></Banner>
      </div>

    </div>

  </div>
</template>

<script setup>
import Banner from "@/components/home/Banner.vue"
import LeftMenu from "@/components/home/LeftMenu.vue";
</script>

<style scoped lang="less">
.nav {
  .main {
    padding-top: 15px;
    width: var(--content-width);
    margin: 0 auto;
    .banner {
      margin-left: 220px;
    }
  }
}
</style>