<template>
    <div class="main">
        <div class="category clearfix">
            <!--    {{goods}}-->
            <div class="goods fl" v-for="(item,index) in goods"
                 :key="index"
                 @click="toGoodsDetail(item.sku_id)">

                <div class="first-row">
                    <img :src="item.image" alt="">
                </div>

                <div class="second-row dian2">
                    {{ item.name }}
                </div>

                <div class="third-row">
                    <small>￥</small>
                    <span>{{ item.jd_price }}</span>
                </div>

            </div>
        </div>
    </div>

</template>

<script setup>
import {onMounted, ref, watch} from "vue";
import {getCategoryGoods} from "@/network/home.js"
import {toGoodsDetail} from "@/utils/goods.js";

let categoryId = defineProps(["categoryId"])
let goods = ref([]);

// 页面，翻页，现在是第几页
let page = ref(1);
onMounted(() => {
    getCategoryGoodsData(1, 1);
})
const getCategoryGoodsData = (categoryId, page) => {
    getCategoryGoods(categoryId, page).then((res) => {
        let serverData = res.data;
        for (let i in serverData) {
            let jsonData = JSON.parse(serverData[i]);
            goods.value.push(jsonData);
        }

    })
}

watch(categoryId, (newVal, oldVal) => {
    // console.log(newVal.categoryId);
    // 这里每次都要重置
    goods.value = []
    getCategoryGoodsData(newVal.categoryId, 1);
    page.value = 1;
})

    const windowScroll=()=> {
    // 当前区域高度
    let clientHeight = document.documentElement.clientHeight;

    // 滚动条在页面的高度
    let scrollTop = document.documentElement.scrollTop;

    // 所有内容的高度
    let scrollHeight = document.body.scrollHeight;

    if (clientHeight + scrollTop >= clientHeight) {
        // console.log(categoryId.categoryId)
        page.value+=1;
        getCategoryGoodsData(categoryId.categoryId, page.value)
    }
}
    window.addEventListener("scroll", windowScroll);

</script>

<style scoped lang="less">
.main {
    margin-top: 10px;

    .category {
        width: var(--content-width);
        margin: 0 auto;

        .goods {
            background-color: #fff;
            width: 232px;
            height: 320px;
            margin-bottom: 10px;
            transition: all 0.3s ease;

            &:hover{
                cursor: pointer;
                .first-row img {
                    opacity: 0.6;
                }
                .second-row {
                    color: #F30213;
                }
            }
            &:not(:nth-child(5n)) {
                margin-right: 10px;
            }

            .first-row {        // 图片大小，两个230 可以调一下
                height: 230px;
                line-height: 230px;
                text-align: center;
                img {
                    width: 150px;
                    height: 150px;
                }
            }

            .second-row {
                width: 190px;
                height: 40px;
                font-size: 14px;
                line-height: 20px;
                margin: 0 auto;
                color: #666;
            }

            .third-row {
                color: #f30213;
                font-size: 20px;
                font-weight: 700;
                text-align: left;

                margin-top: 10px;
                margin-left: 20px;
            }
        }
    }
}

</style>