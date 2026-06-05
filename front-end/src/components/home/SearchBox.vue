<template>
  <div class="main">
    <div class="content">
      <input
        type="text"
        placeholder="找点什么好东西……"
        ref="searchWord"
        @keyup.enter="handleEnterKey"
        v-model="searchInput"
      >
      <span class="iconfont icon-chaxun" @click="handleSearch"></span>
      <div class="hotwords">
        <a
          v-for="(item, key) in hotWords"
          :key="key"
          :class="item.active ? 'active' : ''"
          @click.prevent="handleHotWordSearch(item.word)"
          href="#"
        >
          {{ item.word }}
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();
const searchWord = ref(null);
const searchInput = ref("");

let hotWords = ref([
  {"word": "暖冬好物 国补立减50%", "active": true},
  {"word": "电脑", "active": false},
  {"word": "美", "active": false},
	{"word": "护肤", "active": false},
  {"word": "女士", "active": false},
  {"word": "速食", "active": false},
])

// 从路由 路径参数中获取关键词
const extractKeywordFromRoute = () => {
  if (route.params.keyword) {
    searchInput.value = decodeURIComponent(route.params.keyword);
  }
}

onMounted(() => {
  extractKeywordFromRoute();
});

// 搜索框显示当前搜索词
watch(() => route.params.keyword, () => {
  extractKeywordFromRoute();
});

const search = (keyword) => {
  if (!keyword || keyword.trim() === "") {
    // console.log("搜索内容不能为空");
    return;
  }

  // 对关键词进行编码，确保特殊字符不会破坏URL
  const encodedKeyword = encodeURIComponent(keyword.trim());
  router.push(`/goods_list/${encodedKeyword}/1/1`);
}

// 回车键 和 点击搜索
const handleEnterKey = () => {
  handleSearch();
}
const handleSearch = () => {
  search(searchInput.value);
}


const handleHotWordSearch = (word) => {
  searchInput.value = word;
  // 不跳转
  if (word === "暖冬好物 国补立减50%") {
    return;
  }

  search(word);
}
</script>



<style scoped lang="less">
@red: #e2231a;
.main {
  height: 100%;
  margin-top: 45px;

  .content {
    width: 550px;
    height: 35px;
    border: 2px solid @red;
    margin-left: 80px;

    input {
      width: 485px;
      height: 35px;
      line-height: 35px;
      padding-left: 15px;
    }

    span {
      display: inline-block;
      background-color: @red;
      width: 50px;
      height: 35px;
      line-height: 35px;
      text-align: center;
      color: white;
      font-weight: 800;

      &:hover {
        cursor: pointer;
        background-color: #E64548;
      }
    }
    .hotwords{
      margin-top: 10px;
      font-size: 14px;
      a{
        // #FF0F23 active红色
        // #505259 灰色
        color: #505259;
        margin-right: 10px;
        &:hover{
          color: #FF0F23;
        }
      }
      .active{
        color: @red;
      }
    }
  }
}

</style>