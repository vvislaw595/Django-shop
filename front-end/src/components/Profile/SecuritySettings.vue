<template>
  <div class="basic_info">
    <table>
      <tr>
        <td class="table-key">
          <span>旧密码：</span>
        </td>
        <td class="table-value">
            <el-input type="password"
                      v-model="oldPassword"
                      placeholder="请输入密码"></el-input>
        </td>
      </tr>

      <tr>
        <td class="table-key">
          <span>新密码：</span>
        </td>
        <td class="table-value">
            <el-input type="password"
                      v-model="newPassword"
                      placeholder="请输入密码"></el-input>
        </td>
      </tr>

      <tr>
        <td class="table-key">
          <span>请再次输入新密码：</span>
        </td>
        <td class="table-value">
          <el-input type="password"
                    v-model="secNewPassword"
                    placeholder="请输入密码"></el-input>
        </td>
      </tr>

      <tr>
        <td class="table-key">
        </td>
        <td class="submit">
          <el-button type="success" @click="changePassword">提交</el-button>
        </td>
      </tr>
    </table>
  </div>
</template>

<script setup>
  import {ref} from "vue";
  import {changePasswordRequest} from "@/network/user.js";
  import { ElMessage } from 'element-plus';

  let oldPassword = ref("");
  let newPassword = ref('');
  let secNewPassword = ref('');

  const validateInputs = () => {
    if(!oldPassword.value.trim()){
      ElMessage.error("旧密码不能为空");
      return false;
    }
    if(!newPassword.value.trim()){
      ElMessage.error("新密码不能为空");
      return false;
    }
    if(!secNewPassword.value.trim()){
      ElMessage.error("确认新密码不能为空");
      return false;
    }
    if(newPassword.value !== secNewPassword.value){
      ElMessage.error("两次输入的新密码不一致");
      return false;
    }
		if(newPassword.value.length < 6){
    ElMessage.error("新密码长度至少为6个字符");
    return false;
  }

  const forbiddenPasswords = ['111111', '123456'];

  if(forbiddenPasswords.includes(newPassword.value)){
    ElMessage.error("密码过于简单");
    return false;
  }
    return true;
  }

  const changePassword = () => {
    if(!validateInputs()){
      return;
    }

    changePasswordRequest({
      old_password: oldPassword.value,
      new_password: newPassword.value,
      confirm_password: secNewPassword.value,
    })
    .then((res) => {
      // 处理成功响应
      if(res.status == 200){
        ElMessage.success("修改密码成功");
        oldPassword.value = "";
        newPassword.value = "";
        secNewPassword.value = "";
      } else {
        // 处理非200状态码（如400错误），显示后端返回的错误信息
        // 后端返回格式通常是 { status: 400, data: "错误信息" }
        const errorMsg = res.data || "修改密码失败";
        ElMessage.error(errorMsg);
      }
    })
  }
</script>

<style scoped lang="less">
  .basic_info{
    background-color: white;
    width: 1000px;
    height: 300px;
    table{
      //margin-top: 20px;
      padding-top: 20px;
      tr{

          .table-key{
            padding-left: 30px;
            font-weight: 700;
          }
          .table-value{
            padding-left: 1px;
          }
          .submit{
            padding-top: 20px;
            padding-left: 161px;
          }
      }
    }


  }
</style>