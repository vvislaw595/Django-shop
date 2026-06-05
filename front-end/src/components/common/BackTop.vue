<template>
  <div class="back-to-top"
       :class="{ 'show': isVisible }"
       @click="scrollToTop">
    <div class="back-to-top-content">
        <p>回到</p>
      <span class="iconfont icon-top"></span>
        <p>顶部</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isVisible = ref(false);

const handleScroll = () => {
  // 当页面滚动超过300px时显示按钮
  isVisible.value = window.scrollY > 300;
};

// 回到顶部
const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped lang="less">
.back-to-top {
  position: fixed;
  //right: 20px;
	left: 50%;
	margin-left: 660px;
  bottom: 160px;
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  cursor: pointer;
  z-index: 9999;
  padding: 12px 15px;

	//这四个0必须要有，没有的话做不出来动画效果
  height: 0;
  padding-top: 0;
  padding-bottom: 0;
  border-width: 0;
  overflow: hidden;

  transition: all 0.3s ease;

  &.show {
    height: auto;
    padding-top: 12px;
    padding-bottom: 12px;
    border-width: 1px;
  }

  &:hover {
    background-color: red;
    p {
      color: white;
    }
    .iconfont {
      color: white;
    }
  }

  .back-to-top-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    opacity: 0;
    transition: opacity 0.2s ease;
  }

  &.show .back-to-top-content {
    opacity: 1;
    transition-delay: 0.1s;
  }

  p {
    margin: 5px;
    font-size: 12px;
    line-height: 1.2;
    color: #666;
  }

  .iconfont {
    font-size: 18px;
    color: #666;
    margin: 4px 0;
    transition: color 0.3s ease;
  }
}
</style>