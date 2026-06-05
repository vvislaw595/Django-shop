<template>
	<div>
		<Shortcut></Shortcut>
		<div class="order-pay">
			<div class="header">
				<div class="title clearfix">
					<div class="logo fl">
						<Logo></Logo>
					</div>
						<div class="shop-name fl">DOGeast</div>
						<div class="name fl">收银台</div>
				</div>
			</div>

			<div class="order-info">
				<div class="order-num">
					订单提交成功，请尽快付款。订单号：
						<span>{{tradeNo}}</span>
				</div>
				<div class="pay-mode">
					<div>应付金额:
							<span class="pay-count">{{orderAmount}}</span>元
					</div>
					<img src="@/assets/images/order/alipay.png" alt="">支付宝支付
				</div>
				<div class="pay-order">
					<button class="pay-order-button" @click="toAliPay">立即支付</button>
				</div>
			</div>
		</div>

	</div>
</template>

<script setup>
	import Shortcut from "@/components/common/Shortcut.vue";
	import Logo from "@/components/common/Logo.vue";
	import {useRoute,useRouter} from "vue-router";
	import {onMounted, ref} from "vue";
	import {toAliPayPage} from "@/network/order.js";

	const route = useRoute();
	let tradeNo = ref();
	let orderAmount = ref();

	onMounted(() => {
		tradeNo.value = route.query.tradeNo;
		orderAmount.value = route.query.orderAmount;
		console.log("沙箱账号：scvphu3783@sandbox.com");
	})


	const toAliPay = () => {
		let orderData = ref({
			tradeNo:tradeNo.value,
			orderAmount:orderAmount.value,
		})

		let pay_url = ref("");
		toAliPayPage(orderData.value).then(res => {
			pay_url.value = res.alipay;
			window.location.href = pay_url.value;
		})
	}

</script>

<style scoped lang="less">
.order-pay {
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

		.shop-name {
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

	.order-info {
		margin-top: 50px;
		.order-num {
			font-size: 20px;
		}
		.pay-mode{
			font-size: 16px;
			margin-top: 20px;
			padding: 20px;
			.pay-count{
				color: red;
			}
		}
		.pay-order{
			text-align: right;
			margin-top: 20px;
			.pay-order-button{
				margin-right: 200px;
				width: 135px;
				height: 45px;
				line-height: 45px;
				text-align: center;
				background-color: red;
				color: white;
				font-size: 20px;
				font-weight: 700;
				border-radius: 5px;
			}
		}
	}
}
</style>