<template>
	<div class="address">
		<div class="addAddressButton" @click="addAddressDialogFormVisible = true">新增收货地址</div>
		<!--    在这里循环-->
		<div v-if="allAddresses.length === 0"
		     class="no-address-tip"
		     @click="addAddressDialogFormVisible = true">
			<p>您还没有添加收货地址</p>
			<p>点击此处 或者 上面的"新增收货地址"按钮添加一个吧！</p>
		</div>

		<!-- 有地址时显示地址列表 -->
		<div v-else>
			<div class="info" v-for="(item, index) in allAddresses" :key="index">
				<div class="clearfix">
					<span class="title fl">{{ item.signer_name }}</span>
					<div v-if="item.default" class="default fl">默认地址</div>
					<img
						class="fr cs"
						src="@/assets/images/profile/deletex.png"
						alt="删除"
						@click="deleteAddress(item.id)"
					>
				</div>

				<table>
					<tbody>
					<tr>
						<td class="table-key">收货人：</td>
						<td class="table-value">{{ item.signer_name }}</td>
					</tr>

					<tr>
						<td class="table-key">所在地区：</td>
						<td class="table-value">{{ item.district }}</td>
					</tr>

					<tr>
						<td class="table-key">收货地址：</td>
						<td class="table-value">{{ item.signer_address }}</td>
					</tr>

					<tr>
						<td class="table-key">手机：</td>
						<td class="table-value">{{ item.telphone }}</td>
					</tr>

					<!--        <tr class="edit">-->
					<!--          <td class="table-key"></td>-->
					<!--          <td class="table-value">编辑</td>-->
					<!--        </tr>-->
					</tbody>
				</table>
				<span class="edit fr" style="padding-right: 10px;" @click="editAddress(item.id)">编辑</span>
			</div>
		</div>

		<!--	新增收货地址弹窗  -->
		<el-dialog v-model="addAddressDialogFormVisible"
		           title="新增收货地址" width="500"
		           @close="resetForm">
			<el-form :model="form" :rules="formRules" ref="addFormRef">
				<el-form-item label="收货人" :label-width="formLabelWidth" prop="signer_name">
					<el-input v-model="form.signer_name" autocomplete="off" placeholder="请输入收货人姓名"/>
				</el-form-item>

				<el-form-item label="所在地区" :label-width="formLabelWidth" prop="district">
					<el-input v-model="form.district" autocomplete="off" placeholder="请输入所在省市"/>
				</el-form-item>

				<el-form-item label="收货地址" :label-width="formLabelWidth" prop="signer_address">
					<el-input v-model="form.signer_address" autocomplete="off" placeholder="请输入详细地址"/>
				</el-form-item>

				<el-form-item label="联系电话" :label-width="formLabelWidth" prop="telphone">
					<el-input v-model="form.telphone"
					          autocomplete="off"
					          placeholder="请输入11位手机号"
					          maxlength="11"/>
				</el-form-item>

				<el-form-item label="是否设为默认地址" :label-width="formLabelWidth">
					<el-switch v-model="form.default" active-color="#13ce66" inactive-color="#E3E4E5"></el-switch>
				</el-form-item>

			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button @click="addAddressDialogFormVisible = false">取 消</el-button>
					<el-button type="primary" @click="saveNewAddress">
						新 增
					</el-button>
				</div>
			</template>
		</el-dialog>

		<!--	  编辑地址弹出框-->
		<el-dialog v-model="editAddressDialogFormVisible"
		           title="编辑收货地址"
		           width="500"
		           @close="resetEditForm">
			<el-form :model="editAddressInfo" :rules="formRules" ref="editFormRef">
				<el-form-item label="收货人" :label-width="formLabelWidth" prop="signer_name">
					<el-input v-model="editAddressInfo.signer_name" autocomplete="off" placeholder="请输入收货人姓名"/>
				</el-form-item>

				<el-form-item label="所在地区" :label-width="formLabelWidth" prop="district">
					<el-input v-model="editAddressInfo.district" autocomplete="off" placeholder="请输入所在省市"/>
				</el-form-item>

				<el-form-item label="收货地址" :label-width="formLabelWidth" prop="signer_address">
					<el-input v-model="editAddressInfo.signer_address" autocomplete="off" placeholder="请输入详细地址"/>
				</el-form-item>

				<el-form-item label="联系电话" :label-width="formLabelWidth" prop="telphone">
					<el-input v-model="editAddressInfo.telphone"
					          autocomplete="off"
					          placeholder="请输入11位手机号"
					          maxlength="11"/>
				</el-form-item>

				<el-form-item label="是否设为默认地址" :label-width="formLabelWidth">
					<el-switch v-model="editAddressInfo.default" active-color="#13ce66" inactive-color="#E3E4E5"></el-switch>
				</el-form-item>

			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button @click="editAddressDialogFormVisible = false">取 消</el-button>
					<el-button type="primary" @click="updateAddressInfo">
						更 新
					</el-button>
				</div>
			</template>
		</el-dialog>

	</div>

</template>

<script setup>

import {ref, reactive, onMounted} from "vue";
import {addAddressData, deleteAddressData, editAllAddressData, getAllAddressesData} from "@/network/address.js";
import {ElMessage, ElMessageBox} from "element-plus";

const addAddressDialogFormVisible = ref(false)
const editAddressDialogFormVisible = ref(false)
const addFormRef = ref(null);
const editFormRef = ref(null);
const formLabelWidth = '140px'

const form = reactive({
	signer_name: "",
	district: "",
	signer_address: "",
	telphone: "",
	default: true
})


// 表单验证规则
const formRules = {
	signer_name: [
		{required: true, message: '请输入收货人姓名', trigger: 'blur'},
	],
	district: [
		{required: true, message: '请输入所在地区', trigger: 'blur'},
	],
	signer_address: [
		{required: true, message: '请输入收货地址', trigger: 'blur'},
	],
	telphone: [
		{required: true, message: '请输入联系电话', trigger: 'blur'},
		{pattern: /^1[3-9]\d{9}$/, message: '请输入11位有效的手机号码', trigger: 'blur'}
	]
};


const saveNewAddress = () => {
	if (!addFormRef.value) return;

	addFormRef.value.validate((valid) => {
		if (valid) {
			// 验证通过
			addAddressData(form).then((res) => {
				if (res.status == 200) {
					ElMessage.success("保存成功");
					getAllAddresses();
					addAddressDialogFormVisible.value = false;
				}
			})
		} else {
			ElMessage.warning("请正确填写所有必填字段");
			return false;
		}
	});
}

let allAddresses = ref([])
const getAllAddresses = () => {
	getAllAddressesData().then(res => {
		allAddresses.value = res.data;
	})

}

onMounted(() => {
	getAllAddresses();
})


// 删除收货地址
const deleteAddress = (addressId) => {
	// 使用 Element Plus 的确认框
	ElMessageBox.confirm(
		'确定要删除这个收货地址吗？',
		'提示',
		{
			confirmButtonText: '确定',
			cancelButtonText: '取消',
			type: 'warning',
		}
	)
		.then(() => {
			deleteAddressData({id: addressId}).then((res) => {
				if (res.status == 200) {
					ElMessage.success("删除成功");
					getAllAddresses();
				} else {
					ElMessage.error(res.message || "删除失败");
				}
			})
		})
		.catch(() => {
			// 取消就什么都不做
			ElMessage.info("已取消删除");
		});
};


// 编辑收货地址

let editAddressInfo = reactive({
	id: "",
	signer_name: "",
	district: "",
	signer_address: "",
	telphone: "",
	default: false
})

const editAddress = (id) => {
  const address = allAddresses.value.find(item => item.id == id);
  if (address) {
    // 复制地址信息到编辑表单
    Object.assign(editAddressInfo, {
      id: address.id,
      signer_name: address.signer_name,
      district: address.district,
      signer_address: address.signer_address,
      telphone: address.telphone,
      default: address.default == 1 || address.default === true
    });
    editAddressDialogFormVisible.value = true;
  }
}


const updateAddressInfo = () => {
  if (!editFormRef.value) return;

  editFormRef.value.validate((valid) => {
    if (valid) {
      // 验证通过
      editAllAddressData(editAddressInfo).then((res) => {
        if (res.status === 200) {
          ElMessage.success("更新成功");
          getAllAddresses();
          editAddressDialogFormVisible.value = false;
        }
      })}
else {
      ElMessage.warning("请正确填写所有必填字段");
      return false;
    }
  });
}


// 重置新增表单
const resetForm = () => {
  if (addFormRef.value) {
    addFormRef.value.resetFields();
  }
  Object.assign(form, {
    signer_name: "",
    district: "",
    signer_address: "",
    telphone: "",
    default: true
  });
};

// 重置编辑表单
const resetEditForm = () => {
  if (editFormRef.value) {
    editFormRef.value.resetFields();
  }
  Object.assign(editAddressInfo, {
    id: "",
    signer_name: "",
    district: "",
    signer_address: "",
    telphone: "",
    default: false
  });
};


</script>

<style scoped lang="less">
.address {
	padding-top: 20px;
	padding-left: 20px;
	padding-bottom: 20px;
	width: 880px;

	.addAddressButton {
		//margin-top: 20px;

		width: 115px;
		height: 30px;
		background-color: #f0f9e9;
		text-align: center;
		line-height: 30px;
		border: 1px solid #bfd6af;
		font-weight: 700;

		&:hover {
			cursor: pointer;
			background-color: #F0F9E9;
		}
	}

	.no-address-tip {
		text-align: center;
		padding: 50px 20px;
		margin-right: 20px;
		color: #999;
		background-color: #f9f9f9;
		margin-top: 20px;

		&:hover {
			cursor: pointer;
			background-color: #ededed;
		}
	}

	.no-address-tip p:first-child {
		font-size: 18px;
		margin-bottom: 10px;
	}

	.no-address-tip p:last-child {
		font-size: 14px;
	}

	.info {
		margin-top: 10px;
		border: 2px solid #e6e6e6;
		width: 830px;
		height: 175px;

		> div {
			padding: 10px;
		}

		.title {
			font-size: 14px;
			color: #666;
		}

		.default {
			margin-left: 20px;
			width: 55px;
			height: 20px;
			line-height: 20px;
			text-align: center;
			background-color: #ffaa45;
			color: #fff;
		}

		img {
			width: 18px;
			height: 18px;
		}

		table {

			margin-left: 30px;

			tr {
				td {
					padding-bottom: 10px;
				}
			}

			.table-key {
				text-align: left;
				color: #999999;
			}

			.table-value {
				padding-left: 10px;
				//width: 710px;
			}

		}

		.edit {
			color: #005ea7;

			&:hover {
				cursor: pointer;
				color: red;
			}
		}

	}
}
</style>