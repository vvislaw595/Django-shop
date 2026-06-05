<template>
  <div class="register">
    <div class="title clearfix">
      <div class="logo fl">
        <Logo></Logo>
      </div>
      <div class="name fl">DOGeast</div>
      <div class="name fl">用户注册</div>
    </div>
    <div class="register-info">
      <div class="register-content">
        <div class="register-text">
          <div class="title">
            <img src="@/assets/images/login/warning.png" alt="">
            请填写以下信息完成注册
          </div>
          <div class="register-name">
            用户注册
          </div>

          <!-- 用户名输入 -->
          <div class="register-name1">
            <label for="name">
              <img src="@/assets/images/login/username.png" alt="">
            </label>
            <input type="text" id="username"
                   placeholder="请输入用户名"
                   v-model="registerForm.name"
                   @blur="validateField('name')">
            <span class="error-text" v-if="errors.name">{{ errors.name }}</span>
          </div>

          <!-- 密码输入 -->
          <div class="register-password">
            <label for="password">
              <img src="@/assets/images/login/password.png" alt="">
            </label>
            <input type="password" id="password"
                   placeholder="请输入密码（至少6位）"
                   v-model="registerForm.password"
                   @blur="validateField('password')">
            <span class="error-text" v-if="errors.password">{{ errors.password }}</span>
          </div>

          <!-- 确认密码输入 -->
          <div class="register-password">
            <label for="confirmPassword">
              <img src="@/assets/images/login/password.png" alt="">
            </label>
            <input type="password" id="confirmPassword"
                   placeholder="请再次输入密码"
                   v-model="registerForm.confirmPassword"
                   @blur="validateField('confirmPassword')">
            <span class="error-text" v-if="errors.confirmPassword">{{ errors.confirmPassword }}</span>
          </div>

          <!-- 手机号输入 -->
          <div class="register-mobile">
            <label for="mobile">
              <img src="@/assets/images/login/phone.png" alt="">
            </label>
            <input type="text" id="mobile"
                   placeholder="请输入手机号"
                   v-model="registerForm.mobile"
                   maxlength="11"
                   @blur="validateField('mobile')">
            <span class="error-text" v-if="errors.mobile">{{ errors.mobile }}</span>
          </div>

          <!-- 邮箱输入 -->
          <div class="register-email">
            <label for="email">
              <img src="@/assets/images/login/email.png" alt="">
            </label>
            <input type="email" id="email"
                   placeholder="请输入邮箱"
                   v-model="registerForm.email"
                   @blur="validateField('email')">
            <span class="error-text" v-if="errors.email">{{ errors.email }}</span>
          </div>

          <!-- 图片验证码 -->
          <div class="register-captcha">
            <label for="captcha">
              <img src="@/assets/images/login/captcha.png" alt="">
            </label>
            <input type="text" id="captcha"
                   placeholder="请输入图片验证码"
                   v-model="registerForm.captcha"
                   maxlength="4"
                   style="width: 180px;"
                   @blur="validateField('captcha')">
            <div class="captcha-img" @click="refreshCaptcha" :title="captchaLoading ? '加载中...' : '点击刷新验证码'">
              <img v-if="captchaImage" :src="captchaImage" alt="验证码" class="captcha-image" />
              <span v-else-if="captchaLoading">加载中...</span>
              <span v-else>点击获取验证码</span>
            </div>
            <span class="error-text" v-if="errors.captcha">{{ errors.captcha }}</span>
          </div>

          <!-- 邮箱验证码 -->
          <div class="register-email-code">
            <label for="emailCode">
              <img src="@/assets/images/login/email.png" alt="">
            </label>
            <input type="text" id="emailCode"
                   placeholder="请输入邮箱验证码"
                   v-model="registerForm.emailCode"
                   maxlength="6"
                   style="width: 180px;"
                   @blur="validateField('emailCode')">
            <button class="send-code-btn"
                    @click="sendEmailCode"
                    :disabled="!canSendEmailCode || sendingEmailCode || countdown > 0"
                    :class="{ 'disabled': !canSendEmailCode || sendingEmailCode || countdown > 0 }">
              {{ sendBtnText }}
            </button>
            <span class="error-text" v-if="errors.emailCode">{{ errors.emailCode }}</span>
          </div>

          <!-- 错误消息 -->
          <div class="error-message" v-if="errorMessage">
            {{ errorMessage }}
          </div>

          <!-- 注册按钮 -->
          <button class="register-commit" @click="handleRegister" :disabled="registering">
            {{ registering ? '注册中...' : '立即注册' }}
          </button>

          <!-- 登录链接 -->
          <div class="login-link">
            已有账号？<router-link to="/login">立即登录</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import Logo from "@/components/common/Logo.vue";
import {
  getCaptchaRequest,
  sendEmailCodeRequest,
  registerRequest
} from "@/network/user.js";

const router = useRouter();

// 注册表单数据
const registerForm = reactive({
  name: "",
  email: "",
  mobile: "",
  password: "",
  confirmPassword: "",
  captcha: "",
  emailCode: ""
});

// 错误消息对象
const errors = reactive({
  name: "",
  email: "",
  mobile: "",
  password: "",
  confirmPassword: "",
  captcha: "",
  emailCode: ""
});

// 全局错误消息
const errorMessage = ref("");

// 验证码图片
const captchaImage = ref("");
const captchaLoading = ref(false);

// 邮箱验证码相关状态
const countdown = ref(0);
const countdownInterval = ref(null);
const sendingEmailCode = ref(false);

// 注册状态
const registering = ref(false);

// 验证规则
const validationRules = {
  name: (value) => {
    if (!value.trim()) return "用户名不能为空";
		if (value.length > 10) return "用户名长度不能超过10个字符";
    return "";
  },
  email: (value) => {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!value.trim()) return "邮箱不能为空";
    if (!emailRegex.test(value)) return "邮箱格式不正确";
    return "";
  },
  mobile: (value) => {
    const mobileRegex = /^1[3-9]\d{9}$/;
    if (!value.trim()) return "手机号不能为空";
    if (!mobileRegex.test(value)) return "手机号格式不正确";
    return "";
  },
  password: (value) => {
    if (!value.trim()) return "密码不能为空";
    if (value.length < 6) return "密码至少6个字符";
		if (value === "111111" || value === "123456") return "密码过于简单";
    return "";
  },
  confirmPassword: (value) => {
    if (!value.trim()) return "请再次输入密码";
    if (value !== registerForm.password) return "两次输入的密码不一致";
    return "";
  },
  captcha: (value) => {
    if (!value.trim()) return "验证码不能为空";
    if (value.length !== 4) return "验证码必须为4位";
    return "";
  },
  emailCode: (value) => {
    if (!value.trim()) return "邮箱验证码不能为空";
    if (value.length !== 6) return "验证码必须为6位";
    return "";
  }
};

// 计算属性：是否可以发送邮箱验证码
const canSendEmailCode = computed(() => {
  return registerForm.email && registerForm.captcha && !errors.email && !errors.captcha;
});

// 计算属性：发送按钮文本
const sendBtnText = computed(() => {
  if (countdown.value > 0) {
    return `${countdown.value}秒后重新发送`;
  }
  return sendingEmailCode.value ? "发送中..." : "发送验证码";
});

// 获取图片验证码
const fetchCaptcha = async () => {
  captchaLoading.value = true;
  try {
    const res = await getCaptchaRequest();
    // console.log(res.data.captcha_text);

    if (res.status === 200) {
      captchaImage.value = res.data.image_data;
      errorMessage.value = "";

    } else {
      errorMessage.value = "获取验证码失败，请重试";
      // console.error('验证码获取失败，状态码:', res.status);
    }
  } catch (error) {
    // console.error("获取验证码失败:", error);
    // console.error("错误详情:", error.response);
    errorMessage.value = "获取验证码失败，请刷新页面重试";
  } finally {
    captchaLoading.value = false;
  }
};

// 刷新验证码
const refreshCaptcha = () => {
  if (!captchaLoading.value) {
    fetchCaptcha();
    registerForm.captcha = "";
    errors.captcha = "";
  }
};

// 发送邮箱验证码
const sendEmailCode = async () => {
  if (!canSendEmailCode.value || sendingEmailCode.value || countdown.value > 0) {
    return;
  }

  // 验证邮箱和验证码
  const emailError = validationRules.email(registerForm.email);
  const captchaError = validationRules.captcha(registerForm.captcha);

  if (emailError || captchaError) {
    errors.email = emailError;
    errors.captcha = captchaError;
    return;
  }

  sendingEmailCode.value = true;
  errorMessage.value = "";

  try {
    const res = await sendEmailCodeRequest({
      email: registerForm.email,
      captcha: registerForm.captcha
    });

    if (res.status == 200) {
      // 开始倒计时
      startCountdown();
      errorMessage.value = "";
      alert("验证码发送成功，请查看邮箱");
    } else {
      errorMessage.value = res.data || "验证码发送失败";
    }
  } catch (error) {
    console.error("发送验证码失败:", error);
    errorMessage.value = "验证码发送失败，请重试";
  } finally {
    sendingEmailCode.value = false;
  }
};

// 开始倒计时
const startCountdown = () => {
  countdown.value = 60;
  clearInterval(countdownInterval.value);

  countdownInterval.value = setInterval(() => {
    countdown.value--;
    if (countdown.value <= 0) {
      clearInterval(countdownInterval.value);
    }
  }, 1000);
};

// 验证单个字段
const validateField = (fieldName) => {
  const value = registerForm[fieldName];
  const rule = validationRules[fieldName];

  if (rule) {
    errors[fieldName] = rule(value);
  }
};

// 验证所有字段
const validateAllFields = () => {
  let isValid = true;
  errorMessage.value = "";

  Object.keys(validationRules).forEach(fieldName => {
    const error = validationRules[fieldName](registerForm[fieldName]);
    errors[fieldName] = error;
    if (error) {
      isValid = false;
    }
  });

  return isValid;
};

// 处理注册
const handleRegister = async () => {
  if (registering.value) return;

  // 验证所有字段
  if (!validateAllFields()) {
    errorMessage.value = "请检查表单中的错误";
    return;
  }

  registering.value = true;
  errorMessage.value = "";

  try {
    // 准备注册数据（注意字段名与后端对应）
    const registerData = {
      name: registerForm.name,
      email: registerForm.email,
      mobile: registerForm.mobile,
      password: registerForm.password,
      confirm_password: registerForm.confirmPassword, // 注意：后端需要confirm_password
      captcha: registerForm.captcha,
      email_code: registerForm.emailCode // 注意：后端需要email_code
    };

    const res = await registerRequest(registerData);

    if (res.status == 200) {
      // 注册成功
      alert("注册成功！");
      // 跳转到登录页
      router.push("/login");
    } else {
      errorMessage.value = res.data || "注册失败";
    }
  } catch (error) {
    console.error("注册失败:", error);
    errorMessage.value = "注册失败，请稍后重试";
  } finally {
    registering.value = false;
  }
};

onMounted(() => {
  fetchCaptcha();
});

onUnmounted(() => {
  // 清理定时器
  if (countdownInterval.value) {
    clearInterval(countdownInterval.value);
  }
});
</script>

<style scoped lang="less">
.register {
  .title {
    width: 1000px;
    height: 80px;
    line-height: 80px;
    margin: 0 auto;
    .logo {
      height: 40px;
    }
    .name {
      font-size: 36px;
      font-weight: 700;
      margin-left: 20px;
      margin-top: 30px;
    }
  }

  .register-info {
    margin-top: 43px;
    background-color: #e93854;
    .register-content {
      width: 990px;
      height: 580px; /* 增加高度以适应更多字段 */
      margin: 0 auto;
      background-image: url("@/assets/images/login/sb2.png");
      .register-text {
        //width: 450px;
        width: 500px;       // 500是为了适配 “用户名长度不能超过20个字符”
        height: 580px;
        background-color: #fff;
        float: right;
        //margin-top: 20px;
        padding: 10px;
        box-sizing: border-box;
        position: relative;
        border: 1px solid #bdbdbd;



        .title {
          background-color: #fff8f0;
          width: 100%;
          height: 30px;
          line-height: 30px;
          text-align: center;
          color: #999;
          font-size: 14px;
          margin-top: -10px;
          img {
            width: 16px;
            height: 16px;
            vertical-align: middle;
            margin-right: 5px;
          }
        }

        .register-name {
          width: 100%;
          height: 40px;
          line-height: 40px;
          text-align: center;
          color: #e93854;
          font-size: 18px;
          font-weight: 700;
          border-bottom: 2px solid #f4f4f4;
          margin-bottom: 15px;
        }

        .register-name1,
        .register-password,
        .register-email,
        .register-mobile,
        .register-captcha,
        .register-email-code {
          border: 1px solid #bdbdbd;
          width: 320px;
          height: 40px;
          line-height: 40px;
          margin-bottom: 15px;
          position: relative;
          display: flex;
          align-items: center;

          label {
            display: inline-block;
            width: 40px;
            height: 38px;
            line-height: 38px;
            text-align: center;
            border-right: 1px solid #bdbdbd;
            background-color: #f4f4f4;
            flex-shrink: 0;
            img {
              height: 20px;
              width: 20px;
              vertical-align: middle;
            }
          }

          input {
            padding-left: 10px;
            border: none;
            outline: none;
            flex-grow: 1;
            height: 38px;
            font-size: 14px;
          }

          .error-text {
            position: absolute;
            left: 326px;
            color: #ff0000;
            font-size: 12px;
            white-space: nowrap;
          }
        }

        .register-captcha,
        .register-email-code {
          input {
            width: 180px;
            flex-grow: 0;
          }

          .captcha-img {
            flex-grow: 1;
            height: 38px;
            line-height: 38px;
            text-align: center;
            background-color: #f8f8f8;
            border-left: 1px solid #bdbdbd;
            cursor: pointer;
            color: #666;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;

            .captcha-image {
              width: 100%;
              height: 100%;
              object-fit: cover;
            }

            &:hover {
              background-color: #f0f0f0;
            }
          }

          .send-code-btn {
            flex-grow: 1;
            height: 38px;
            line-height: 38px;
            border: none;
            background-color: #e93854;
            color: white;
            font-size: 14px;
            cursor: pointer;
            margin-left: 5px;
            border-radius: 3px;
            transition: background-color 0.3s;

            &:hover:not(.disabled) {
              background-color: #d32f4a;
            }

            &.disabled {
              background-color: #cccccc;
              cursor: not-allowed;
              opacity: 0.7;
            }
          }
        }

        .error-message {
          color: #ff0000;
          font-size: 14px;
          text-align: center;
          margin: 10px 0;
          min-height: 20px;
        }

        .register-commit {
          width: 100%;
          height: 45px;
          background-color: #FA2C19;
          color: #fff;
          margin-bottom: 10px;
          font-size: 20px;
          font-weight: 700;
          border-radius: 5px;
          border: none;
          cursor: pointer;
          transition: background-color 0.3s;

          &:hover:not(:disabled) {
            background-color: #e02615;
          }

          &:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
            opacity: 0.7;
          }
        }

        .login-link {
          font-size: 14px;
          font-weight: 700;
          text-align: center;


          a {
            color: #e93854;
            text-decoration: none;

            &:hover {
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