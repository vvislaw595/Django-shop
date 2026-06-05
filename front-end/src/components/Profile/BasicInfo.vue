<template>
	<div class="basic_info">
		<el-alert
			v-if="message"
			:title="message"
			:type="messageType"
			show-icon
			closable
			@close="message = ''"
			style="margin-bottom: 20px;"
		/>

		<table>
			<tr>
				<td class="table-key">
					<span>昵称：</span>
				</td>
				<td class="table-value">
					<el-input
						v-model="formData.name"
						placeholder="请输入昵称"
						maxlength="20"
						show-word-limit
					></el-input>
				</td>
			</tr>

			<tr>
				<td class="table-key">
					<span>性别：</span>
				</td>
				<td class="table-value">
					<el-radio-group v-model="formData.gender">
						<el-radio label="男" size="default">男</el-radio>
						<el-radio label="女" size="default">女</el-radio>
						<el-radio label="保密" size="default">保密</el-radio>
					</el-radio-group>
				</td>
			</tr>

			<tr>
				<td class="table-key">
					<span>生日：</span>
				</td>
				<td class="table-value">
					<el-date-picker
						v-model="formData.birthday"
						type="date"
						placeholder="请选择日期"
						value-format="YYYY-MM-DD"
						format="YYYY-MM-DD"
					></el-date-picker>
				</td>
			</tr>

			<tr>
				<td class="table-key"></td>
				<td class="submit">
					<el-button
						type="success"
						:loading="loading"
						@click="handleSubmit"
					>
						提交
					</el-button>
				</td>
			</tr>
		</table>
	</div>
</template>

<script setup>
import {ref, onMounted} from "vue";
import {getProfileRequest, updateProfileRequest} from "@/network/user";
import {ElMessage} from 'element-plus';
import store from "@/store";


const formData = ref({
	name: "",
	gender: "保密",
	birthday: "2010-01-01"
});

const loading = ref(false);
const message = ref("");
const messageType = ref("");

// 获取用户信息 数据回显
const fetchUserProfile = async () => {
	const response = await getProfileRequest();

	if (response.status === 200) {
		const userData = response.data;

		// 更新表单数据
		if (userData.name) formData.value.name = userData.name;
		if (userData.gender) formData.value.gender = userData.gender;
		if (userData.birthday) formData.value.birthday = userData.birthday;
		if(userData.name){
			store.commit("setUserName", userData.name);
		}
	}
};

// 提交表单
const handleSubmit = async () => {
	// 验证必填字段
	if (!formData.value.name || formData.value.name.trim() === "") {
		showMessage("昵称不能为空", "error");
		return;
	}

	// loading.value = true;

	const response = await updateProfileRequest(formData.value);

	if (response.status === 200) {
		showMessage(response.data?.message || "更新成功", "success");
		store.commit("setUserName", formData.value.name);
		await fetchUserProfile();
	}

	// loading.value = false;  // 关闭提交按钮的加载动画
};

// 显示消息
const showMessage = (msg, type) => {
	message.value = msg;
	messageType.value = type;

	setTimeout(() => {
		message.value = "";
	}, 3000);
};

onMounted(() => {
	fetchUserProfile();
});
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