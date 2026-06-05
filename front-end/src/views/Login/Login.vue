<template>
  <div class="login">
    <div class="title clearfix">
        <div class="logo fl">
          <Logo></Logo>
        </div>
      <div class="name fl">DOGeast</div>
      <div class="name fl">欢迎登录</div>
    </div>
    <div class="login-info">
      <div class="login-content">
        <div class="login-text">
          <div class="title">
            <img src="@/assets/images/login/warning.png" alt="">
            谨防诈骗谨防诈骗谨防诈骗谨防诈骗谨防诈骗
          </div>
          <div class="login-name">
            账户登录
          </div>
          <div class="login-username">
            <label for="username">
              <img src="@/assets/images/login/username.png" alt="">
            </label>
            <input type="text" id="username"
                   placeholder="请输入登录邮箱"
                   v-model="userInfo.username">
          </div>
          <div class="login-password">
            <label for="password">
              <img src="@/assets/images/login/password.png" alt="">
            </label>
            <input type="password" id="password"
                   placeholder="请输入密码"
                   v-model="userInfo.password">
          </div>
          <a href="/reset" class="forget-password">忘记密码</a>
          <button class="login-commit" @click="login">登录</button>
          <div class="register">
            <a href="/register">立即注册</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Logo from "@/components/common/Logo.vue";
import {loginRequest} from "@/network/user.js";
import {reactive} from "vue";
import {useStore} from "vuex";
import {useRouter} from "vue-router";

const router = useRouter();
const store = useStore();

let userInfo = reactive({
  username: "",
  password: "",
})

const login = () => {
  // console.log(userInfo);
  loginRequest(userInfo).then((res) => {
    if(res.status == 200){
      alert("登录成功");
      // 存储在本地
      window.localStorage.setItem("token",res.data.token);
      window.localStorage.setItem("username",res.data.username);
      store.commit("setLogin",true);
      store.commit("setUserName",res.data.username);

			// is_staff 判断是不是管理员，但是还要is_superuser才行
			store.commit('setIsSuperuser', res.data.is_superuser);

      router.push("/");
			// 弹窗出来点击确定之后，登录进去主页面要马上刷新，不然会显示上一个用户名字
			setTimeout(() => {
				location.reload();
			}, 0)
    }
    else {
      alert(res.data);
    }
    console.log(res.status);
    console.log(res.data);
  })
}
</script>

<style scoped lang="less">
.login{
  //background-color: #F5F6FA;
  .title{
    width: 1000px;
    height: 80px;
    line-height: 80px;
    margin: 0 auto;
    .logo{
      height: 40px;
    }
    .name{
      font-size: 36px;
      font-weight: 700;
      margin-left: 20px;
      margin-top: 30px;
    }
  }
  .login-info{
    margin-top: 43px;
    background-color: #e93854;

    .login-content{
      width: 990px;
      height: 480px;
      margin: 0 auto;
      background-image: url("@/assets/images/login/sb.png");
      .login-text{
        width: 350px;
        height: 350px;
        background-color: #fff;
        float: right;
        margin-top: 20px;
        .title{
          background-color: #fff8f0;
          width: 350px;
          height: 40px;
          line-height: 40px;
          text-align: center;
          color: #999;
          img{
            width: 16px;
            height: 16px;

          }
        }
        .login-name{
          width: 350px;
          height: 40px;
          line-height: 40px;
          text-align: center;
          color: #e93854;
          font-size: 18px;
          font-weight: 700;
          border-bottom: 2px solid #f4f4f4;
        }
        .login-username,.login-password{
          border: 1px solid #bdbdbd;
          width: 310px;
          height: 40px;
          line-height: 40px;
          margin: 25px auto 0;
          label{
            display: inline-block;
            width: 40px;
            //height: 40px;
            line-height: 40px;
            text-align: center;
            border-right: 1px solid #bdbdbd ;
            background-color: #f4f4f4;
            img{
              height: 20px;
              width: 20px;
            }
          }
          input{
            padding-left: 10px;
          }
        }

        .forget-password{
          position: relative;
          right: -270px;
          bottom: -84px;
          text-align: right;
          color: #666;
          font-size: 14px;
          width: 310px;
            &:hover{
              color: #ff8ba3;
              border-bottom: 1px solid #ff0f23;
            }
        }
        .login-commit{
          width: 310px;
          height: 40px;
          background-color: #FA2C19;
          color: #fff;
          margin-top: 10px;
          font-size: 20px;
          margin-left: 20px;
          font-weight: 700;
          border-radius: 5px;
        }
        .register{
          font-size: 14px;
          font-weight: 700;
          background-color: #fcfcfc;
          height: 50px;
          width: 310px;
          margin-left: 20px;
          line-height: 50px;
          text-align: left;
          a{
            color: #e93854;
            &:hover{
              color: #ff8ba3;
              border-bottom: 1px solid #ff0f23;
            }
          }
        }
      }

    }
  }
}
</style>