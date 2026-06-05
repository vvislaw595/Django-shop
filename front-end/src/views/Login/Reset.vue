<template>
  <div class="register">
    <div class="title clearfix">
      <div class="logo fl">
        <Logo></Logo>
      </div>
      <div class="name fl">DOGeast</div>
      <div class="name fl">忘记密码</div>
    </div>
    <div class="reset-info">
      <div class="reset-content">
        <div class="reset-text">
          <div class="title">
            <img src="@/assets/images/login/warning.png" alt="">
            请填写以下信息重置密码
          </div>
          <div class="reset-name">
            忘记密码
          </div>

          <!-- 邮箱输入 -->
          <div class="reset-email">
            <label for="email">
              <img src="@/assets/images/login/email.png" alt="">
            </label>
            <input type="email" id="email"
                   placeholder="请输入要找回密码的邮箱"
                   v-model="resetForm.email"
                   @blur="validateField('email')">
            <span class="error-text" v-if="errors.email">{{ errors.email }}</span>
          </div>

          <!-- 图片验证码 -->
          <div class="reset-captcha">
            <label for="captcha">
              <img src="@/assets/images/login/captcha.png" alt="">
            </label>
            <input type="text" id="captcha"
                   placeholder="请输入图片验证码"
                   v-model="resetForm.captcha"
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
          <div class="reset-email-code">
            <label for="emailCode">
              <img src="@/assets/images/login/email.png" alt="">
            </label>
            <input type="text" id="emailCode"
                   placeholder="请输入邮箱验证码"
                   v-model="resetForm.emailCode"
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

          <!-- 密码输入 -->
          <div class="reset-password">
            <label for="password">
              <img src="@/assets/images/login/password.png" alt="">
            </label>
            <input type="password" id="password"
                   placeholder="请输入密码（至少6位）"
                   v-model="resetForm.password"
                   @blur="validateField('password')">
            <span class="error-text" v-if="errors.password">{{ errors.password }}</span>
          </div>

          <!-- 确认密码输入 -->
          <div class="reset-password">
            <label for="confirmPassword">
              <img src="@/assets/images/login/password.png" alt="">
            </label>
            <input type="password" id="confirmPassword"
                   placeholder="请再次输入密码"
                   v-model="resetForm.confirmPassword"
                   @blur="validateField('confirmPassword')">
            <span class="error-text" v-if="errors.confirmPassword">{{ errors.confirmPassword }}</span>
          </div>



          <!-- 错误消息 -->
          <div class="error-message" v-if="errorMessage">
            {{ errorMessage }}
          </div>

          <!-- 重置密码按钮 -->
          <button class="reset-commit" @click="handleReset" :disabled="reseting">
            {{ reseting ? '重置密码中...' : '重置密码' }}
          </button>

          <!-- 登录链接 -->
          <div class="login-link">
            想起密码了？<router-link to="/login">立即登录</router-link>
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
import {getCaptchaRequest, forgetEmailCodeRequest, resetRequest} from "@/network/user.js";

const router = useRouter();

// 重置密码表单数据
const resetForm = reactive({
  email: "",
	captcha: "",
  emailCode: "",
  password: "",
  confirmPassword: ""
});

// 错误消息对象
const errors = reactive({
  email: "",
	captcha: "",
  emailCode: "",
  password: "",
  confirmPassword: ""
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

// 重置密码状态
const reseting = ref(false);

// 验证规则
const validationRules = {
  email: (value) => {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!value.trim()) return "邮箱不能为空";
    if (!emailRegex.test(value)) return "邮箱格式不正确";
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
    if (value !== resetForm.password) return "两次输入的密码不一致";
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
  return resetForm.email && resetForm.captcha && !errors.email && !errors.captcha;
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

    if (res.status === 200) {
      captchaImage.value = res.data.image_data;
      errorMessage.value = "";

    } else {
      errorMessage.value = "获取验证码失败，请重试";

    }
  } catch (error) {

    errorMessage.value = "获取验证码失败，请刷新页面重试";
  } finally {
    captchaLoading.value = false;
  }
};

// 刷新验证码
const refreshCaptcha = () => {
  if (!captchaLoading.value) {
    fetchCaptcha();
    resetForm.captcha = "";
    errors.captcha = "";
  }
};

// 发送邮箱验证码
const sendEmailCode = async () => {
  if (!canSendEmailCode.value || sendingEmailCode.value || countdown.value > 0) {
    return;
  }

  // 验证邮箱和验证码
  const emailError = validationRules.email(resetForm.email);
  const captchaError = validationRules.captcha(resetForm.captcha);

  if (emailError || captchaError) {
    errors.email = emailError;
    errors.captcha = captchaError;
    return;
  }

  sendingEmailCode.value = true;
  errorMessage.value = "";

  try {
    const res = await forgetEmailCodeRequest({
      email: resetForm.email,
      captcha: resetForm.captcha
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
  const value = resetForm[fieldName];
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
    const error = validationRules[fieldName](resetForm[fieldName]);
    errors[fieldName] = error;
    if (error) {
      isValid = false;
    }
  });

  return isValid;
};

// 处理重置密码
const handleReset = async () => {
  if (reseting.value) return;

  // 验证所有字段
  if (!validateAllFields()) {
    errorMessage.value = "请检查表单中的错误";
    return;
  }

  reseting.value = true;
  errorMessage.value = "";

  try {
    // 准备重置密码数据（注意字段名与后端对应）
    const resetData = {
      email: resetForm.email,
	    captcha: resetForm.captcha,
      email_code: resetForm.emailCode,
      new_password: resetForm.password,
      confirm_password: resetForm.confirmPassword,
    };

    const res = await resetRequest(resetData);

    if (res.status == 200) {
      // 重置密码成功
      alert("密码重置成功，请使用新密码登录");
      // 跳转到登录页
      router.push("/login");
    } else {
      errorMessage.value = res.data || "重置密码失败";
    }
  } catch (error) {
    console.error("重置密码失败:", error);
    errorMessage.value = "重置密码失败，请稍后重试";
  } finally {
    reseting.value = false;
  }
};

// 生命周期钩子
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

  .reset-info {
    margin-top: 43px;
    background-color: #e93854;
    .reset-content {
      width: 990px;
      height: 580px; /* 增加高度以适应更多字段 */
      margin: 0 auto;
      background-image: url("@/assets/images/login/sb2.png");
      .reset-text {
        width: 450px;
        height: 465px;
        background-color: #fff;
        float: right;
        margin-top: 20px;
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

        .reset-name {
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

        .reset-name1,
        .reset-password,
        .reset-email,
        .reset-mobile,
        .reset-captcha,
        .reset-email-code {
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

        .reset-captcha,
        .reset-email-code {
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

        .reset-commit {
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