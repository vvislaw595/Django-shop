<template>
  <div class="left-menu" @mouseleave="noItem()">
    <ul>
      <!--{{showMainData}}-->
      <li v-for="(item,index) in showMainData" :key="index"
      @mouseenter="showItem(item,index)">
      <span v-for="(d,i) in item.data" :key="i">
        <a :href="'/goods_list/'+d.name+'/1/1'">{{ d.name }}</a>
        <span v-if="item.data.length-i-1"> / </span>

      </span>
      </li>

    </ul>
    <div class="second-item" v-show="isShowItem">
<!--      二级菜单 showSecondMenuIndex-->
      <SecondMenu :showSecondMenuIndex="showSecondMenuIndex"></SecondMenu>
    </div>
  </div>
</template>

<script setup>
import {getMainMenu} from "@/network/home.js"
import {computed, onMounted, ref} from "vue";
import SecondMenu from "@/components/home/SecondMenu.vue";


let leftMenuData = ref([])
onMounted(() => {
  getMainMenu().then(res => {
    // console.log(res)
    init_menu_data(res.data);
  })
})

const init_menu_data = (menuData) => {
  // console.log(menuData);
  for (let i in menuData) {
    let jsonData = JSON.parse(menuData[i])
    leftMenuData.value.push(jsonData)
  }
}
// 接口返回数据需要进行加工，
// 基本结构应该是[{index:1,data:[{name,url},{},{} ]}]
const showMainData = computed(() => {
  let resultList = []
  let result = {"index": "", "data": []};
  for (let i in leftMenuData.value) {
    let id = leftMenuData.value[i].main_menu_id;
    let data = {"name": leftMenuData.value[i].main_menu_name}

    if (result["index"] != null && id == result["index"]) {
      result["data"].push(data);
    } else {
      result = {"index": "", "data": []};
      result["index"] = id;
      result["data"].push(data);
      resultList.push(result);
    }
  }
  return resultList;
})


// 二级菜单显示和隐藏
let isShowItem = ref(false);
let showSecondMenuIndex = ref();
// 显示二级菜单
const showItem = (index) => {
  isShowItem.value = true;
  showSecondMenuIndex.value = index;
}
// 隐藏
const noItem = ()=>{
  isShowItem.value = false;
}

</script>

<style scoped lang="less">
.left-menu {
  position: relative;
  background-color: #fff;
  width: 210px;
  height: 480px;

  ul {
    padding-top: 15px;

    li {
      //padding-top: 5px;
      //padding-bottom: 5px;
      padding-left: 20px;
      line-height: 25px;
      height: 25px;

      &:hover {
        cursor: pointer;
        background-color: #d9d9d9;
      }

      a {
        font-size: 14px;
        color: #1A1A1A;

        &:hover {
          cursor: pointer;
          color: #ff0f23;
        }
      }
    }
  }

  .second-item {
    position: absolute;
    top: 0px;
    left: 210px;
    z-index: 999;
  }
}
</style>