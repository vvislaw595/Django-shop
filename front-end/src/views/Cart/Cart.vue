<template>
	<div class="shop_cart">
		<Shortcut></Shortcut>
		<Header_test></Header_test>
		<div class="goods">
			<div class="goods_num">
				全部商品&nbsp;&nbsp;{{ cartSumNums }}
			</div>
			<table>
				<thead>
				<tr>
					<th>
						<input type="checkbox" :checked="allChecked" @click="checkedAll">全选
					</th>
					<th>商品</th>
					<th></th>
					<th>单价</th>
					<th>数量</th>
					<th>小计</th>
					<th>操作</th>
				</tr>
				</thead>


				<!--        这里写循环-->
				<tbody>
				<tr v-for="(item,key) in cartListData" :key="key">
					<td>
						<input type="checkbox"
						       :checked="item.checked"
						       @click="changeChecked(item.sku_id)">
					</td>
					<td>
						<img :src="item.goods.image" alt="">
					</td>
					<td>{{ item.goods.name }}</td>
					<td>￥{{ item.goods.p_price }}</td>
					<td>
						<el-input-number
							v-model="item.nums"
							@change="(newVal,oldVal)=>handleChange(newVal,oldVal,item.sku_id)"
							:min="1"
							:max="10"
							label=""></el-input-number>
					</td>
					<!--          保留两位小数-->
					<td>￥{{ (item.goods.p_price * item.nums).toFixed(2) }}</td>
					<td>
						<el-popconfirm
							width="200"
							confirm-button-text="删除"
							cancel-button-text="不，谢谢"
							title="确定删除这个订单吗？"
							@confirm="deleteCartItem(item.sku_id)">
							<template #reference>
								删除
							</template>
						</el-popconfirm>
					</td>
				</tr>
				</tbody>

			</table>

			<div class="bottom_tool">
				<div class="tool_left">
					<input type="checkbox" :checked="allChecked" @click="checkedAll">全选
					<span class="delete_selected" @click="deleteGoods(0)">删除选中商品</span>
					<span class="clear_cart" @click="deleteGoods(1)">清空购物车</span>
				</div>
				<div class="tool_right">
					<span class="selected_goods">已选择 <em>{{ selectedGoodsCount }}</em>件商品</span>
					<span class="price_count">总价： <em>￥{{ priceCount.toFixed(2) }}</em></span>
					<button
					   class="go_order"
					   :class="{ 'disabled': selectedGoodsCount === 0 }"
					   @click="goOrder">去结算</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import Shortcut from "@/components/common/Shortcut.vue";
import Header_test from "@/components/home/Header_test.vue";
import {getCartDetailData, updateCartGoodsNumData, deleteCartGoods} from "@/network/cart.js";
import {onMounted, ref, watch} from "vue";
import {useStore} from "vuex";
import {createOrderData, updateOrderInfoData} from "@/network/order.js";
import {useRouter} from "vue-router";
import {ElMessage} from "element-plus";


const router = useRouter();
let cartListData = ref([])
let cartSumNums = ref(0)


onMounted(() => {
	getCartDetailData().then((res) => {
		console.log(res.data)
		cartListData.value = res.data
		// 计算商品总数
		for (let i in res.data) {
			cartSumNums.value += res.data[i].nums;
		}
	})
	store.dispatch("updateCart")
})

// 修改购物车商品数量
const store = useStore();
const handleChange = (newVal, oldVal, skuId) => {
	console.log(newVal, oldVal, skuId)
	let data = ref({
		nums: newVal,
		sku_id: skuId
	})
	// 更新商品数量
	updateCartGoodsNumData(data.value).then((res) => {
		// console.log(res)
		store.dispatch("updateCart");
		// 这样有问题 不能这样写
		// cartSumNums.value = store.state.cartCount+parseInt(1)
	})
	cartSumNums.value += newVal - oldVal;
}

// 全选
let allChecked = ref(false);
const checkedAll = () => {
	// 点了全选
	if (allChecked.value == false) {
		for (let i in cartListData.value) {
			cartListData.value[i].checked = true;
		}
		allChecked.value = true;
		// 更新 已选择 0件商品
		selectedGoodsCount.value = cartListData.value.length;
	}
	// 取消全选
	else {
		for (let i in cartListData.value) {
			cartListData.value[i].checked = false;
		}
		allChecked.value = false;
		selectedGoodsCount.value = 0;
	}
}
// 计算商品
let selectedGoodsCount = ref(0);
let priceCount = ref(0);

watch(() => cartListData, (newVal, oldVal) => {
	// console.log(cartListData);
	priceCount.value = 0;
	cartSumNums.value = 0;
	cartListData.value.forEach((element) => {
		if (element.checked) {
			priceCount.value += element.goods.p_price * element.nums;
		}
		cartSumNums.value += element.nums;
	})


}, {
	deep: true,   // 深度监听参数，加上才能监听到ref里面的列表，列表里面json
})

// 单个商品选中
const changeChecked = (id) => {
	for (let i in cartListData.value) {
		if (cartListData.value[i].sku_id == id) {   // 取反
			cartListData.value[i].checked = !cartListData.value[i].checked;
		}
		selectedGoodsCount.value = 0;
		cartListData.value.forEach((element) => {
			if (element.checked == true) {
				selectedGoodsCount.value += 1;
			}
		})
		// 更新全选：全部单个勾完了之后，全选也勾上
		if (selectedGoodsCount.value == cartListData.value.length) {
			allChecked.value = true;
		} else {
			allChecked.value = false;
		}
	}
}


let deleteGoodsList = ref([])   // 记下要删除的商品
let noDeleteGoodsList = ref([])    // 第二种

// 移出购物车
const deleteGoods = (deleteStatus) => {
	// console.log(deleteGoodsList.value)
	deleteGoodsList.value = []
	noDeleteGoodsList.value = []

	if (deleteStatus == 0) {
		cartListData.value.forEach((element) => {
			if (element.checked) {
				deleteGoodsList.value.push(element.sku_id)
			} else {
				noDeleteGoodsList.value.push(element)  // 第二种else三行
			}
		})

		if (deleteGoodsList.value.length == 0) {
			alert("请先选择要删除的商品")
		} else {
			let res = confirm("确认要将商品移除出购物车吗？");
			if (res) {
				deleteCartGoods(deleteGoodsList.value).then((res) => {
					alert("删除商品成功");
					// 第一种方法，直接刷新
					// location.reload();

					// 第二种，cartListData.value重新赋值，动态渲染
					cartListData.value = noDeleteGoodsList.value

					store.dispatch("updateCart");

					selectedGoodsCount.value = 0;

				})
			} else {
				alert("取消删除");
			}
		}
	}
	// 清空购物车
	else {
		if(cartListData.value.length == 0) {
			alert("购物车内没有商品")
			return;
		}
		let res = confirm("确定要清空购物车吗？");
		if (res) {
			cartListData.value.forEach((element) => {
				deleteGoodsList.value.push(element.sku_id)

			})// 请求后端接口
			deleteCartGoods(deleteGoodsList.value).then((res) => {
				alert("已清空购物车，回到首页");
				// 第一种方法，直接刷新
				// location.reload();

				// 第二种，cartListData.value重新赋值，动态渲染
				cartListData.value = noDeleteGoodsList.value

				// store.dispatch("updateCart");                // 不调用它了，直接
				store.commit("updateCartCount", {count: 0});  // 强制设置为0
				window.localStorage.setItem("count", "0");                // 清空本地存储

				selectedGoodsCount.value = 0;
				// 清空完购物车回到首页
				location.href = "/"

			})
		} else {
			alert("取消删除");
		}
	}

}


// 删除单个购物车商品
const deleteCartItem = (skuId) => {
  deleteCartGoods([skuId]).then((res) => {
    ElMessage.success({
      message: "删除成功",
      type: "success"
    });

    // 从列表中移除该商品
    const index = cartListData.value.findIndex(item => item.sku_id === skuId);
    if (index !== -1) {
      cartListData.value.splice(index, 1);
    }

    // 更新购物车数量
    store.dispatch("updateCart");
  })
	// setTimeout(() => {
	// 			location.reload();
	// 		}, 800)
}


// 去结算 创建订单
let orderGoodsList = ref([])
const goOrder = () => {
	if(selectedGoodsCount.value === 0){
		return;
	}
	for (let i in cartListData.value) {
		if (cartListData.value[i].checked == true) {
			orderGoodsList.value.push(cartListData.value[i]);
		}
	}
	let orderData = ref({
		trade: {
			order_amount: priceCount.value,
		},
		goods: orderGoodsList.value
	})
	// 向后端发送请求
	let orderNo = ref("")
	createOrderData(orderData.value).then((res) => {
		orderNo.value = res.data.trade_no;
		router.push("/order/" + orderNo.value);
		store.dispatch("updateCart");
	})
}

</script>

<style scoped lang="less">
.shop_cart {
	.goods {
		width: var(--content-width);
		margin: 0 auto;

		.goods_num {
			color: #e2231a;
			font-size: 16px;
			font-weight: 700;
		}

		table {
			border-collapse: collapse;
			width: 100%; // 没有100%和下面那些，在没有商品的时候撑不开
			tr {
				border-bottom: 1px solid #f0f0f0;

				th {
					background-color: #f3f3f3;
					height: 45px;
					//全选78.19
					//商品82
					//空574.91
					//单价79.14
					//数量150
					//小计118.25
					//操作117.52
					&:nth-child(1) {
						width: 55px;
						padding-left: 24px;
					}

					&:nth-child(2) {
						width: 82px
					}

					&:nth-child(3) {
						width: 575px
					}

					&:nth-child(4) {
						width: 79px
					}

					&:nth-child(5) {
						width: 150px
					}

					&:nth-child(6) {
						width: 118px
					}
				}

				td {
					padding-top: 10px;
					padding-bottom: 10px;

					img {
						width: 80px;
						height: 80px;
						border: 1px solid #eeeeee;
					}

					&:nth-child(1) {
						text-align: center;
					}

					&:nth-child(3) {
						width: 465px;
						padding-left: 20px;
						padding-right: 100px;

						&:hover {
							color: #e2231a;
							cursor: pointer;
						}
					}

					&:nth-child(4) {
						text-align: center;
						width: 80px;
					}

					&:nth-child(5) {
						text-align: center;
						width: 80px;
					}

					&:nth-child(6) {
						text-align: center;
						width: 120px;
						font-weight: 700;
					}

					&:nth-child(7) {
						text-align: center;
						width: 120px;

						&:hover {
							cursor: pointer;
							color: red;
						}
					}
				}
			}
		}

		.bottom_tool {
			border: 1px solid #f0f0f0;
			margin-top: 10px;
			height: 50px;
			line-height: 50px;

			.tool_left {
				float: left;
				padding-left: 29px;

				span {
					padding: 0 10px;

					&:hover {
						color: #e2231a;
						cursor: pointer;
					}
				}

				.clear_cart {
					font-size: 14px;
					font-weight: 700;
				}
			}

			.tool_right {
				float: right;
				text-align: right;

				span {
					font-weight: 700;
					color: #acacac;

					em {
						color: #e2231a;
						font-weight: 700;
						padding: 0 5px;
					}
				}

				.price_count {
					em {
						font-size: 16px;

					}
				}

				.go_order {
					display: inline-block;
					width: 95px;
					height: 50px;
					line-height: 50px;
					text-align: center;
					color: #fff;
					background-color: #e2231a;
					font-size: 18px;
					font-weight: 700;
				}

				.go_order.disabled {
					background-color: #ccc;
					cursor: not-allowed;
					//pointer-events: none;
				}
			}
		}
	}
}
</style>