<template>
  <div class="comment">
    <div v-if="commentData && commentData.length>0">
      <div class="detail " v-for="(item,index) in commentData" :key="index">
        <div class="clearfix">
          <div class="left fl">
            <div class="header_content">
              <img :src="'http://'+item.user_image_url" alt="">
              <span class="nick_name">{{ item.nickname }}</span>
            </div>
          </div>

          <div class="right fl">
            <div class="star">
              <img src="@/assets/images/goods/star.png" alt="" v-for="index in item.score">
              <img src="@/assets/images/goods/star1.png" alt="" v-for="index in (5-item.score)">
            </div>
            <div class="text">
              {{ item.content }}
            </div>
            <div class="time">
              {{ item.create_time.replace("T", " ").replace("Z", " ") }}
            </div>
          </div>
      </div>
      <hr>
      <!--          {{commentData}}-->
    </div>

    <div class="change_page">
      <el-pagination background
                     layout="prev, pager, next"
                     :total="commentCount"
                     :page-size="15"
                     :current-page="currentPage"
                     @current-change="handleCurrentChange"
                     class="custom-pagination"/>
    </div>

    </div>
    <div v-else class="no_comment">
      <hr>
      <span>暂无评论</span>
    </div>

      <BackTop></BackTop>
  </div>
</template>

<script setup>
import {onMounted, ref} from "vue";
import {getCommentCountData, getCommentDetailData} from "@/network/comment.js"
import BackTop from "@/components/common/BackTop.vue";

let skuId = defineProps(["skuId"])
let commentData = ref([]);
let commentCount = ref(0);

onMounted(() => {
  // console.log(skuId);
  getCommentCountData(skuId.skuId).then(res => {
    commentCount.value = res.data;
  })
  getCommentDetailData(skuId.skuId, 1).then(res => {
    commentData.value = res.data;
  })
})

let currentPage = ref(1);


const handleCurrentChange = (page) => {
  currentPage.value = page;
    getCommentDetailData(skuId.skuId, page).then(res => {
    commentData.value = res.data;

		window.scrollTo({
    top: 380,
    behavior: 'smooth'
  });
  })
};

</script>

<style scoped lang="less">
.comment {
  .detail {
    margin-top: 10px;

    .left {
      .header_content {
        img {
          height: 25px;
          width: 25px;
          border-radius: 25px;
        }

        .nick_name {
          margin-left: 10px;
        }
      }
    }

    .right {
      width: 830px;
      margin-left: 70px;

      .star {
        img {
          width: 14px;
          height: 14px;
        }
      }

      .text {
        color: #333;
        font-size: 14px;
        margin-top: 10px;
      }

      .time {
        color: #999;
        margin-top: 10px;
      }
    }

    hr {
      margin-top: 10px;
      margin-bottom: 10px;
      border: 1px solid #dddddd;
    }
  }
      .change_page{
      margin-top: 50px;
      margin-bottom: 100px;
      margin-left: 34%;
      --el-color-primary: red;
    }
  .no_comment {
    text-align: center;
    padding: 40px 0;
    color: #999;
    font-size: 16px;
  }
}
</style>