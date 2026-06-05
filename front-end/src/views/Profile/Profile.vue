<template>
  <div>
	  <back-top></back-top>
    <shortcut></shortcut>
    <div class="profile">
      <div class="header">
        <div class="title clearfix">
          <div class="logo fl">
            <Logo></Logo>
          </div>
          <div class="shop_name fl">DOGeast</div>
          <div class="name fl">个人中心</div>
          <div class="cart fr">
            <shop-cart></shop-cart>
          </div>
        </div>
      </div>

      <div class="main clearfix">
        <div class="content">
          <div class="left_menu fl">
            <div class="basic"
                 :class="activeIndex==1?'active-menu':false"
                 @click="changeComponent(1)">
              基本信息</div>

            <div class="address"
                 :class="activeIndex==2?'active-menu':false"
                 @click="changeComponent(2)">
              地址管理</div>

            <div class="order"
                 :class="activeIndex==3?'active-menu':false"
                 @click="changeComponent(3)">
              我的订单</div>

            <div class="security"
                 :class="activeIndex==4?'active-menu':false"
                 @click="changeComponent(4)">
              修改密码</div>
          </div>

          <div class="right_content fl">
<!--              <component :is="activeComponentName"></component>-->
            <BasicInfo v-if="activeIndex === 1" />
            <AddressManager v-if="activeIndex === 2" />
            <MyOrder v-if="activeIndex === 3" />
            <SecuritySettings v-if="activeIndex === 4" />
          </div>
        </div>


      </div>
    </div>


  </div>
</template>

<script setup>
import ShopCart from "@/components/home/ShopCart.vue";
import Shortcut from "@/components/common/Shortcut.vue";
import Logo from "@/components/common/Logo.vue";
import AddressManager from "@/components/Profile/AddressManager.vue";
import BasicInfo from "@/components/Profile/BasicInfo.vue";
import MyOrder from "@/components/Profile/MyOrder.vue";
import SecuritySettings from "@/components/Profile/SecuritySettings.vue";
import {useRoute,useRouter} from "vue-router";
import {onMounted, reactive, ref} from "vue";
import BackTop from "@/components/common/BackTop.vue";


const route = useRoute();
const router = useRouter();
let activeComponentName = ref("BasicInfo");
let activeIndex = ref(1);
let activeComponent = ref([
  {index:1,componentName:"BasicInfo"},
  {index:2,componentName:"AddressManager"},
  {index:3,componentName:"MyOrder"},
  {index:4,componentName:"SecuritySettings"},
]);

const changeComponent = (index)=>{
  activeIndex.value=index;
  // activeComponent.value.forEach((element)=>{
  //   if(element.index==activeIndex.value){
  //     activeComponentName.value=element.componentName;
  //   }
  // })
  router.push("profile?activeIndex="+index);
}

onMounted(()=>{
  activeIndex.value = parseInt(route.query.activeIndex) || 1;
  // activeComponent.value.forEach((element)=>{
  //   if(element.index==activeIndex.value){
  //     activeComponentName.value=element.componentName;
  //   }
  // })
})

</script>

<style scoped lang="less">
.profile {
  .header {
    height: 130px;
    //line-height: 150px;
    border-bottom: 2px solid red;
  }

  .title {
    width: var(--content-width);
    margin: 0 auto;
    height: 80px;
    line-height: 80px;

    .logo {
      height: 40px;
    }

    .shop_name {
      font-size: 40px;
      font-weight: 700;
      margin-left: 10px;
      margin-top: 30px;
      color: red;
    }

    .name {
      font-size: 25px;
      //font-weight: 700;
      margin-left: 10px;
      margin-top: 30px;
    }
  }

  > .main {
    background-color: #f5f5f5;
    .content {
      width: var(--content-width);
      margin: 0 auto;

      .left_menu {
        color: #333;
        font-size: 14px;
        margin-top: 20px;
        height: 800px;
        div{
          margin-top: 20px;
          border-bottom: 1px solid #f5f5f5;
          &:hover{
            cursor: pointer;
            color: red;
            border-bottom: 1px solid red;
          }
        }
      }
      .active-menu{
        color: red;
      }
      .right_content {
        margin-top: 30px;
        margin-left: 20px;
        background-color: #fff;
      }
    }

  }
}
</style>