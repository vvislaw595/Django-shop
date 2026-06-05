<template>
	<div class="main">
		<a href="/cart/detail">
			<div class="shopcart">

				<el-badge :value="this.$store.state.cartCount" class="item">
					<span class="iconfont icon-gouwuche"></span>
				</el-badge>

				<span>购物车</span>
			</div>
		</a>
	</div>
</template>

<script setup>

</script>

<style scoped lang="less">
.main {
	//height: 140px;
	margin-top: 45px;
	margin-left: 20px;

	a {
		.shopcart {
			border: 1px solid #e3e4e5;
			width: 130px;
			height: 35px;
			line-height: 35px;
			text-align: center;
			font-size: 14px;
			padding-top: 4px;

			.item {
				height: 25px;
				line-height: 25px;

				> span {
					color: #ff0f23;
					font-weight: 700;
				}
			}

			&:hover {
				cursor: pointer;
				border: 1px solid red;
			}

			// 第二个span 购物车
			> span {
				color: #ff0f23;
				font-size: 16px;
				font-weight: 600;
				margin-left: 20px;
			}
		}
	}

}
</style>