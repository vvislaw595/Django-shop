<template>
  <div class="warpper">
    <div class="header">
      <span v-if="this.$store.state.user.isLogin==false">
          <a href="/login">您好，请登录</a>|&nbsp;&nbsp;
          <a href="/register" class="reg">免费注册</a>
      </span>

      <span v-else>
          <a href="/profile?activeIndex=1" class="username">{{this.$store.state.user.name}}</a>欢迎您的使用&nbsp;&nbsp;|&nbsp;&nbsp;
          <a href="/profile?activeIndex=3">我的订单</a> |&nbsp;&nbsp;
	      <a v-if="store.state.user.is_superuser" href="http://127.0.0.1:8000/admin/"
	         target="_blank" class="admin-link">
          后台管理
        </a>

        <template v-if="store.state.user.is_superuser"> |&nbsp;&nbsp;</template>
        <a href="#" class="logout" @click="logout">退出登录</a>
      </span>

    </div>


  </div>
</template>

<script setup>
import {reactive} from "vue";
import {useStore} from "vuex";
import {useRouter} from "vue-router";

const router = useRouter();
const store = useStore();


const logout = () => {
  window.localStorage.setItem("token", "");
  store.commit("setLogin",false);
  router.push("/");
	setTimeout(() => {
				location.reload();
			}, 0)
}


</script>

<style scoped lang="less">
.warpper {
  font-size: 13px;
  background-color: #e3e4e5;
  height: 30px;

  .header {
    .username{
      color: black;

    }
    width: var(--content-width);
    margin: 0 auto;
    text-align: right;
    line-height: 30px;
    a{
      &:hover{
        color: var(--font-red);
      }
      margin-right: 10px;
    }
    .reg{
      color: var(--font-red);
    }
  }
}
</style>