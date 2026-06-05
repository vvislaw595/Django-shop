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
						<td class="table-value">{{ item.signer_address }}</td>
					</tr>

					<tr>
						<td class="table-key">收货地址：</td>
						<td class="table-value">{{ item.district }}</td>
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

				<el-form-item label="所在地区" :label-width="formLabelWidth" required>
					<el-cascader
						v-model="form.selectedArea"
						:options="areaOptions"
						:props="cascaderProps"
						placeholder="请选择省市区"
						style="width: 100%"
						clearable
						@change="handleAreaChange"
					/>
				</el-form-item>

				<el-form-item label="收货地址" :label-width="formLabelWidth" prop="district">
					<el-input v-model="form.district" autocomplete="off" placeholder="请输入详细地址"/>
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

				<el-form-item label="所在地区" :label-width="formLabelWidth" required>
					<el-cascader
						v-model="editAddressInfo.selectedArea"
						:options="areaOptions"
						:props="cascaderProps"
						placeholder="请选择省市区"
						style="width: 100%"
						clearable
						@change="handleEditAreaChange"
					/>
				</el-form-item>

				<el-form-item label="收货地址" :label-width="formLabelWidth" prop="district">
					<el-input v-model="editAddressInfo.district" autocomplete="off" placeholder="请输入详细地址"/>
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
import { ref, reactive, onMounted } from "vue";
import { addAddressData, deleteAddressData, editAllAddressData, getAllAddressesData } from "@/network/address.js";
import { ElMessage, ElMessageBox } from "element-plus";
import { regionData } from 'element-china-area-data';

const addAddressDialogFormVisible = ref(false);
const editAddressDialogFormVisible = ref(false);
const addFormRef = ref(null);
const editFormRef = ref(null);
const formLabelWidth = '140px';

// 使用 regionData 作为级联选择器的数据源
const areaOptions = ref(regionData);

// 级联选择器配置
const cascaderProps = {
	value: 'value',
	label: 'label',
	children: 'children'
};

// 新增表单
const form = reactive({
	signer_name: "",
	selectedArea: [], // 用于级联选择器，存储编码数组
	signer_address: "", // 省市区文本（不直接绑定，由 selectedArea 转换）
	district: "", // 详细地址
	telphone: "",
	default: true
});

// 编辑表单
const editAddressInfo = reactive({
	id: "",
	signer_name: "",
	selectedArea: [], // 用于级联选择器，存储编码数组
	signer_address: "", // 省市区文本（不直接绑定）
	district: "", // 详细地址
	telphone: "",
	default: false
});

// 表单验证规则
const formRules = {
	signer_name: [
		{ required: true, message: '请输入收货人姓名', trigger: 'blur' },
	],
	district: [
		{ required: true, message: '请输入收货地址', trigger: 'blur' },
	],
	telphone: [
		{ required: true, message: '请输入联系电话', trigger: 'blur' },
		{ pattern: /^1[3-9]\d{9}$/, message: '请输入11位有效的手机号码', trigger: 'blur' }
	]
};

// 根据编码获取对应的文本名称
const getAreaNameByCode = (code) => {
	// 递归查找
	const findName = (data, targetCode) => {
		for (const item of data) {
			if (item.value === targetCode) {
				return item.label;
			}
			if (item.children) {
				const found = findName(item.children, targetCode);
				if (found) return found;
			}
		}
		return '';
	};

	return findName(regionData, code);
};

// 新增表单地区选择变化
const handleAreaChange = (value) => {
	if (value && value.length === 3) {
		// 将编码转换为文本
		const province = getAreaNameByCode(value[0]);
		const city = getAreaNameByCode(value[1]);
		const area = getAreaNameByCode(value[2]);
		form.signer_address = province + city + area;
	} else {
		form.signer_address = "";
	}
};

// 编辑表单地区选择变化
const handleEditAreaChange = (value) => {
	if (value && value.length === 3) {
		// 将编码转换为文本
		const province = getAreaNameByCode(value[0]);
		const city = getAreaNameByCode(value[1]);
		const area = getAreaNameByCode(value[2]);
		editAddressInfo.signer_address = province + city + area;
	} else {
		editAddressInfo.signer_address = "";
	}
};

// 保存新地址
const saveNewAddress = () => {
	if (!addFormRef.value) return;

	// 验证省市区是否完整
	if (!form.selectedArea || form.selectedArea.length !== 3) {
		ElMessage.warning("请选择完整的省市区");
		return;
	}

	const submitData = {
		signer_name: form.signer_name,
		signer_address: form.signer_address, // 省市区文本
		district: form.district, // 详细地址
		telphone: form.telphone,
		default: form.default ? 1 : 0
	};

	addFormRef.value.validate((valid) => {
		if (valid) {
			// 验证通过
			addAddressData(submitData).then((res) => {
				if (res.status == 200) {
					ElMessage.success("保存成功");
					getAllAddresses();
					addAddressDialogFormVisible.value = false;
				}
			}).catch(err => {
				ElMessage.error("保存失败");
			});
		} else {
			ElMessage.warning("请正确填写所有必填字段");
			return false;
		}
	});
};

let allAddresses = ref([]);
const getAllAddresses = () => {
	getAllAddressesData().then(res => {
		allAddresses.value = res.data;
	});
};

onMounted(() => {
	getAllAddresses();
});

// 删除收货地址
const deleteAddress = (addressId) => {
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
		deleteAddressData({ id: addressId }).then((res) => {
			if (res.status == 200) {
				ElMessage.success("删除成功");
				getAllAddresses();
			} else {
				ElMessage.error(res.message || "删除失败");
			}
		});
	})
	.catch(() => {
		ElMessage.info("已取消删除");
	});
};

// 根据名称查找编码
const findCodeByName = (name, data = regionData) => {
	for (const item of data) {
		if (item.label === name) {
			return item.value;
		}
		if (item.children) {
			const found = findCodeByName(name, item.children);
			if (found) return found;
		}
	}
	return '';
};

// 将地址文本解析为编码数组
const parseAddressToCodes = (addressText) => {
	if (!addressText || addressText.length < 2) return [];

	// 尝试逐级匹配
	let provinceCode = '';
	let cityCode = '';
	let areaCode = '';

	// 先找省份（通常是前2-3个字符，但为了准确，我们遍历匹配）
	for (const province of regionData) {
		if (addressText.startsWith(province.label)) {
			provinceCode = province.value;
			const remaining = addressText.substring(province.label.length);

			// 查找城市
			for (const city of province.children || []) {
				if (remaining.startsWith(city.label)) {
					cityCode = city.value;
					const areaRemaining = remaining.substring(city.label.length);

					// 查找区县
					for (const area of city.children || []) {
						if (areaRemaining.startsWith(area.label)) {
							areaCode = area.value;
							break;
						}
					}
					break;
				}
			}
			break;
		}
	}

	if (provinceCode && cityCode && areaCode) {
		return [provinceCode, cityCode, areaCode];
	}

	return [];
};

// 编辑收货地址
const editAddress = (id) => {
	const address = allAddresses.value.find(item => item.id == id);
	if (address) {
		// 复制地址信息到编辑表单
		Object.assign(editAddressInfo, {
			id: address.id,
			signer_name: address.signer_name,
			selectedArea: [], // 先清空
			signer_address: address.signer_address, // 保存原始文本
			district: address.district,
			telphone: address.telphone,
			default: address.default == 1 || address.default === true
		});

		// 尝试将地址文本转换为编码数组
		if (address.signer_address) {
			const codeArray = parseAddressToCodes(address.signer_address);
			if (codeArray.length === 3) {
				editAddressInfo.selectedArea = codeArray;
			}
		}

		editAddressDialogFormVisible.value = true;
	}
};

const updateAddressInfo = () => {
	if (!editFormRef.value) return;

	// 验证省市区是否完整
	if (!editAddressInfo.selectedArea || editAddressInfo.selectedArea.length !== 3) {
		ElMessage.warning("请选择完整的省市区");
		return;
	}

	const submitData = {
		id: editAddressInfo.id,
		signer_name: editAddressInfo.signer_name,
		signer_address: editAddressInfo.signer_address, // 省市区文本
		district: editAddressInfo.district, // 详细地址
		telphone: editAddressInfo.telphone,
		default: editAddressInfo.default ? 1 : 0
	};

	editFormRef.value.validate((valid) => {
		if (valid) {
			// 验证通过
			editAllAddressData(submitData).then((res) => {
				if (res.status === 200) {
					ElMessage.success("更新成功");
					getAllAddresses();
					editAddressDialogFormVisible.value = false;
				}
			}).catch(err => {
				ElMessage.error("更新失败");
			});
		} else {
			ElMessage.warning("请正确填写所有必填字段");
			return false;
		}
	});
};

// 重置新增表单
const resetForm = () => {
	if (addFormRef.value) {
		addFormRef.value.resetFields();
	}
	Object.assign(form, {
		signer_name: "",
		selectedArea: [],
		signer_address: "",
		district: "",
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
		selectedArea: [],
		signer_address: "",
		district: "",
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

/* 级联选择器样式调整 */
:deep(.el-cascader) {
	width: 100%;
}

</style>