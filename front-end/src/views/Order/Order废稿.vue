<template>
	<div>

		<shortcut></shortcut>
		<div class="order">
			<div class="header">
				<div class="title clearfix">
					<div class="logo fl">
						<Logo></Logo>
					</div>
					<div class="shop_name fl">DOGeast</div>
					<div class="name fl">结算页面</div>
				</div>
			</div>

			<div class="title-text">填写并核对订单信息</div>
			<div class="order-info ">
				<div class="clearfix">
					<div class="step-title fl">
						<h3>收货人信息</h3>
					</div>
					<div class="add-address fr"  @click="addAddressDialogFormVisible = true">
						新增收货地址
					</div>
				</div>

				<!--		    这里循环-->
				<div class="step-context" v-for="(item,index) in allAddresses" :key="index">
					<span class="address-name cs"
					      :class="item.selected?'selected':''"
					      @click="changeSelected(item.id)">{{ item.signer_name }}</span>
					<span class="address-info">{{ item.signer_address }}</span>
					<span class="address-phone">{{ item.telphone }}</span>
					<span class="address-default" v-show="item.default==1">默认地址</span>
				</div>
				<hr>
				<div class="step-title">
					<h3>支付方式</h3>
				</div>
				<div class="step-context">
					<div class="pay-mode selected">支付宝支付</div>
				</div>
				<hr>
				<div class="step-title">
					<h3>送货清单</h3>
				</div>
				<div class="step-context clearfix">
					<div class="post-mode fl">
						<div>配送方式</div>
						<div class="selected">东风快递</div>
						<div>标准达：<i>预计 12月12日[周五] 9:00-14:00 送达</i></div>
					</div>
					<div class="goods-list fl">
						<!--				    这里循环-->
						<div v-for="(item,index) in goodsInfo" :key="index">
							<div class="goods-shop-name">
								商家：{{ item.shop_name }}
							</div>
							<div>
								<img :src="item.image" alt="">
								<span class="goods-name">{{ item.name }}</span>
								<span class="goods-price">￥{{ item.p_price }}</span>
								<span class="goods-num">x{{ item.goods_num }}</span>
							</div>
						</div>
					</div>
				</div>
			</div>

			<div class="trade-foot">
				<span>应付金额：</span>
				<span class="count-price">￥{{ orderAmount }}</span>
			</div>
			<div class="commit-order">
				<button class="commit-order-button"
				        :class="{ 'disabled': !hasAddress }"
				        @click="handleSubmitOrder">提交订单</button>
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


	</div>
</template>

<script setup>
import {ElMessage, ElMessageBox} from "element-plus";
import {onMounted, reactive, ref, computed} from "vue";
import {useRoute,useRouter} from "vue-router";
import {addAddressData, getAllAddressesData} from "@/network/address.js";
import {getAllOrdersByTradeNo, updateOrderInfoData} from "@/network/order.js";
import ShopCart from "@/components/home/ShopCart.vue";
import AddressManager from "@/components/Profile/AddressManager.vue";
import SecuritySettings from "@/components/Profile/SecuritySettings.vue";
import Shortcut from "@/components/common/Shortcut.vue";
import MyOrder from "@/components/Profile/MyOrder.vue";
import Logo from "@/components/common/Logo.vue";
import BasicInfo from "@/components/Profile/BasicInfo.vue";

const route = useRoute();
const router = useRouter();

// let allAddresses = ref();
let goodsInfo = ref();
let tradeNo = ref();
let orderAmount = ref(0);

onMounted(() => {
	tradeNo.value = route.params.trade_no;

	getAllAddressesData().then((res) => {
		allAddresses.value = res.data;
		// console.log(allAddresses.value);

		allAddresses.value.forEach((element)=>{
			if(element.default==1){
				element.selected=true;
				selectedAddressId.value=element.id;
			}
			else {
				element.selected=false;
			}
		})
	})

	getAllOrdersByTradeNo(tradeNo.value).then((res) => {
		goodsInfo.value = res.data.order_info;
		orderAmount.value = res.data.order_amount;
		console.log(goodsInfo.value)
	})

})
	const addAddressDialogFormVisible = ref(false)
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

const addFormRef = ref(null);
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
					setTimeout(() => {
				location.reload();
			}, 500)
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

	let selectedAddressId = ref();
	const changeSelected=(id)=>{
		allAddresses.value.forEach((element)=>{
				if(element.id==id){
					element.selected=true;
					selectedAddressId.value=id;
				}
				else {
					element.selected=false;
				}
			})
}

	// 计算是否有收货地址
const hasAddress = computed(() => {
  return allAddresses.value && allAddresses.value.length > 0;
});


const handleSubmitOrder = () => {
  // 检查是否有收货地址
  if (!hasAddress.value) {
    alert("请先添一个加收货地址");
    addAddressDialogFormVisible.value = true; // 打开添加地址
    return;
  }

  submitOrder();
};

	const submitOrder=()=>{
		let updateData = ref({
			address_id:selectedAddressId.value,
			trade_no:tradeNo.value,
			pay_status:1
		})

		updateOrderInfoData(updateData.value).then((res)=>{

		})

		router.push({
			name:"OrderPay",
			query:{
				tradeNo:tradeNo.value,
				orderAmount:orderAmount.value,
			}
		})
	}

</script>

<style scoped lang="less">
.order {
	width: var(--content-width);
	margin: 0 auto;

	.header {
		height: 130px;
		//line-height: 150px;
		//border-bottom: 2px solid red;
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

	.title-text {
		line-height: 42px;
		height: 42px;
		font-size: 16px;

	}

	.order-info {
		border: 1px solid #f0f0f0;
		margin-top: 20px;

		.step-title {
			height: 40px;
			line-height: 40px;
			padding-left: 20px;

			h3 {
				font-size: 14px;
				font-weight: 700;
			}
		}

		.add-address {
			color: #005ea7;
			padding-right: 20px;
			padding-top: 20px;

			&:hover {
				color: red;
				cursor: pointer;
			}
		}

		.step-context {
			padding-left: 20px;

			.address-name {
				width: 145px;
				height: 30px;
				line-height: 30px;
				text-align: center;
				display: inline-block;
				border: 1px solid #ddd;
				margin-bottom: 15px;
			}

			.address-info {
				margin-left: 30px;
			}

			.address-phone {
				margin-left: 30px;
			}

			.address-default {
				margin-left: 30px;
				background-color: #ffaa45;
				color: #fff;
				width: 60px;
				height: 25px;
				line-height: 25px;
				text-align: center;
				display: inline-block;
			}
		}

		hr {
			width: 1160px;
			border: 1px solid #f0f0f0;
		}

		.pay-mode {
			width: 100px;
			height: 30px;
			line-height: 30px;
			text-align: center;
			border: 2px solid #f0f0f0;

			&:hover {
				cursor: pointer;
				border: 2px solid red;
			}
		}

		.selected {
			border: 2px solid red !important;
			background-image: url("@/assets/images/order/address-selected.png");
			background-position: 103%;
			background-repeat: no-repeat;
			background-size: 35px;
		}

		.post-mode {
			background-color: #f7f7f7;
			padding: 10px 0px 10px 20px;
			width: 350px;

			div:nth-child(1) {
				font-weight: 700;
			}

			div:nth-child(2) {
				font-weight: 700;
				margin-top: 20px;
				width: 145px;
				height: 30px;
				line-height: 30px;
				text-align: center;

				&:hover {
					cursor: pointer;
				}
			}

			div:nth-child(3) {
				margin-top: 20px;
			}
		}

		.goods-list {
			background-color: #f3fbfe;
			width: 780px;

			.goods-shop-name {
				margin-top: 10px;
				margin-left: 20px;
				font-weight: 700;
			}

			img {
				width: 85px;
				height: 85px;
				margin-top: 10px;
				margin-left: 20px;
				border: 2px solid #d6d1d1;
				//background-color: #fff;
			}

			.goods-name {
				margin-left: 20px;
			}

			.goods-price {
				margin-left: 20px;
				color: red;
				font-weight: 700;

			}

			.goods-num {
				margin-left: 20px;
			}
		}

	}

	.trade-foot {
		background-color: #f4f4f4;
		margin-top: 30px;
		height: 50px;
		line-height: 50px;
		text-align: right;
		padding-right: 40px;
		.count-price{
			color: red;
			font-size: 18px;
			font-weight: 700;
		}
	}
	.commit-order{
		margin-top: 10px;
		margin-bottom: 30px;
		margin-right: 40px;
		text-align: right;
		.commit-order-button{
			width: 135px;
			height: 45px;
			line-height: 45px;
			text-align: center;
			display: inline-block;
			background-color: red;
			color: #fff;
			font-size: 20px;
			font-weight: 700;
			border-radius: 5px;
		}
		.commit-order-button.disabled{
				cursor: not-allowed;
				background-color: #ccc;
			}
	}


}
</style>