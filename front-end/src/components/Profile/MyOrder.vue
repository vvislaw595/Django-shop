<template>
	<div class="order">
		<div class="condition">
			<span v-for="(item,index) in orderStatusDict"
			      :key="index"
			      @click="changeOrderStatus(item.payStatus)"
			      :class="item.isActive?'is-active':''">
				{{ item.payName }}
			</span>
		</div>
		<table>
			<!--这里不知道要不要加thead？ tbody？-->
			<tr class="table-header">
				<th>订单详情</th>
				<th>收货人</th>
				<th>金额</th>
				<th>状态</th>
				<th>操作</th>
			</tr>
			<!---->

			<!--			这里循环-->
			<tbody class="order-info" v-for="(item,index) in goodsInfo" :key="index">
			<!--					占位用的tr 为了解决样式问题-->
			<tr class="blank-tr"></tr>
			<tr class="info-header">
				<td class="order-num">
					<!--							<span>{{item.create_time.replace("T"," ").replace("Z"," ")}}</span>-->
					<span>{{ item.create_time }}</span>
					<span>订单号：</span>
					<b>{{ item.trade_no }}</b>
				</td>

				<td colspan="4" class="img-td">
					<el-popconfirm
						width="200"
						confirm-button-text="删除"
						cancel-button-text="不，谢谢"
						title="确定删除这个订单吗？"
						@confirm="deleteOrder(item.trade_no)">
						<template #reference>
							<img src="@/assets/images/profile/delete.png" alt="">
						</template>
					</el-popconfirm>
				</td>
			</tr>

			<tr class="info-detail" v-for="(data,key) in item.order_info" :key="index">
				<td class="goods-detail clearfix">
					<a :href="'/detail/'+data.sku_id" target="_blank">
						<img :src="data.image" alt="" class="fl">
						<div class="fl">
							<span class="dian2">{{ data.name }}</span>
						</div>
					</a>
					<div class="goods-num fl">x{{data.goods_num}}</div>

				</td>
				<!--						:rowspan="item.order_info.length" v-if="key<1" 表格占多少行-->
				<td :rowspan="item.order_info.length" v-if="key<1">{{ item.address_info?.signer_name || '收货人'}}</td>
				<td :rowspan="item.order_info.length" v-if="key<1">{{ item.order_amount }}</td>
				<td :rowspan="item.order_info.length" v-if="key<1">{{ switchStatus(item.pay_status)[0] }}</td>
				<td :rowspan="item.order_info.length" v-if="key<1">
							<span class="order-action"
							      @click="toAction(item.pay_status,item.trade_no,item.order_amount,item.order_info)">
								{{ switchStatus(item.pay_status)[1] }}
							</span>
				</td>
			</tr>

			</tbody>
		</table>
	</div>
</template>

<script setup>
import {createOrderData, getAllOrder, updateOrderInfoData} from "@/network/order.js";
import {onMounted, reactive, ref} from "vue";
import {useRoute, useRouter} from "vue-router";
import {ElMessage} from "element-plus";

const router = useRouter();

let goodsInfo = ref();
const getAllOrderInfo = (data) => {
	getAllOrder(data).then(res => {
		goodsInfo.value = res.data;
		console.log(goodsInfo.value);
	})
}

onMounted(() => {
	getAllOrderInfo(-1)
})

// 筛选条件变量
const orderStatusDict = ref([
	{
		payStatus: -1,
		payName: "全部订单",
		isActive: true,
	},
	{
		payStatus: 0,
		payName: "待确认",
		isActive: false,
	},
	{
		payStatus: 1,
		payName: "待付款",
		isActive: false,
	},
	{
		payStatus: 2,
		payName: "待收货",
		isActive: false,
	},
	{
		payStatus: 3,
		payName: "已完成",
		isActive: false,
	}
])

const changeOrderStatus = (orderStatus) => {
	orderStatusDict.value.forEach((element) => {
		if (element.payStatus == orderStatus) {
			getAllOrderInfo(orderStatus);
			element.isActive = true;
		} else {
			element.isActive = false;
		}
	})
}

const deleteOrder = (tradeNo) => {
	let updateData = ref({
			trade_no: tradeNo,
			is_delete:1
		})

		updateOrderInfoData(updateData.value).then((res) => {
			ElMessage.success({
				message: "删除成功，刷新页面",
				type: "success"
			});
			setTimeout(() => {
				location.reload();
			}, 800)
		})
}

const toAction = (pay_status, trade_no, order_amount, order_info) => {
	if (pay_status == 0) {
		router.push("/order/" + trade_no);
	} else if (pay_status == 1) {
		router.push({
			name: "OrderPay",
			query: {
				tradeNo: trade_no,
				orderAmount: order_amount
			}
		})
	} else if (pay_status == 2) {
		let updateData = ref({
			trade_no: trade_no,
			pay_status: 3
		})

		updateOrderInfoData(updateData.value).then((res) => {
			ElMessage.success({
				message: "收货成功，刷新页面",
				type: "success"
			});
			setTimeout(() => {
				location.reload();
			}, 800)
		})
	} else if (pay_status == 3) {

		let orderData = ref({
    trade:{
      order_amount:order_amount,
    },
    goods:order_info
  })
  // 向后端发送请求
  let orderNo = ref("")

		createOrderData(orderData.value).then((res) => {
			orderNo.value = res.data.trade_no;
			router.push("/order/" + orderNo.value);
		})
	}
}

const switchStatus = (payStatus) => {
	const orderStatus = reactive({
		0: ["待确认", "确认订单"],
		1: ["待付款", "支付订单"],
		2: ["待收货", "确认收货"],
		3: ["已完成", "再次购买"],
	})
	return orderStatus[payStatus];
}

</script>

<style scoped lang="less">
.order {
	padding: 20px;

	.condition {
		span {
			margin-right: 20px;

			&:hover {
				cursor: pointer;
				color: red;
			}
		}

		.is-active {
			color: red;
			font-weight: 700;
			border-bottom: 2px solid red;
		}
	}

	table {
		width: 900px;
		border-collapse: collapse;
		margin-top: 20px;

		.table-header {
			border: 1px solid #e5e5e5;
			background-color: #f5f5f5;
			height: 35px;

			th:first-child {
				width: 500px;
			}

			th:not(:first-child) {
				width: 100px;
			}
		}

		.order-info {
			//border: 1px solid #e5e5e5;
			.blank-tr {
				height: 20px;
			}

			.info-header {
				border: 1px solid #e5e5e5;
				background-color: #f5f5f5;
				height: 30px;
				color: #aaa;

				.order-num {
					span {
						margin-left: 30px;
					}

					b {
						color: #333;
					}
				}

				.img-td {
					text-align: right;
					padding-right: 42px;

					img {
						width: 15px;
						height: 15px;

						&:hover {
							width: 15px;
							cursor: pointer;
							content: url("@/assets/images/profile/delete-red.png");
						}
					}


				}

			}

			.info-detail {
				border: 1px solid #e5e5e5;

				.goods-detail {
					border: 1px solid #e5e5e5;

					a {
						img {
							width: 60px;
							height: 60px;
							margin-left: 10px;
							//margin-top: 10px;
						}

						div {
							margin-left: 10px;
							padding-top: 10px;
							width: 355px;

							&:hover {
								cursor: pointer;
								color: red;
							}

							span {
								text-align: left;
							}
						}
					}

					.goods-num {
						padding-top: 20px;
						margin-left: 25px;
					}

				}

				td {
					text-align: center;
					border: 1px solid #e5e5e5;
				}

				.order-action {
					display: inline-block;
					border: 1px solid #ddd;
					background-color: #f5f5f5;
					width: 70px;
					height: 30px;
					line-height: 30px;
					text-align: center;

					&:hover {
						cursor: pointer;
						color: red;
						border: 1px solid red;
					}
				}
			}
		}
	}
}
</style>