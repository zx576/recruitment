<template lang="html">
<div class="">

  <!--显示主页  -->
    <div class="bg" v-bind:style="{height: screenHeight + 'px'}">
      <!-- 顶栏-文字-控制按钮 -->
      <div class="top-block">
        <div class="top-left">
          <!-- <img src="../assets/pics/favicon.jpg" alt="编程教室图标" class='favicon'> -->
          <a href="http://crossincode.com" class='c-mainpage'>Crossin的编程教室</a>
          <span class='white'>|</span>
          <span class='white'>Python互联网职位报告</span>
        </div>
        <div class="top-right pull-right">
          <a href="/" class='c-mainpage'>回到主页</a>
          <span class='white'>|</span>
          <a href="#" >
            <span class='glyphicon glyphicon-th-list white' ></span>
            <span class='white'>上海职位地点报告</span>
          </a>
        </div>
      </div>
      <!-- 顶栏-文字-控制按钮  end-->
      <!-- 表显示区域 -->
      <div class="">
        <!-- 表显示 -->
        <div class="display center-block">
            <shanghai-chart></shanghai-chart>
        </div>
      </div>
    </div>
    <!-- 侧边控制栏 -->
    <div class="">

    </div>
</div>

</template>

<script>
import ShanghaiChart from './charts/ShanghaiChart'
export default {
  // mounted: function () {
  //
  // },
  data () {
    return {
      screenHeight: document.documentElement.clientHeight
    }
  },
  components: {
    ShanghaiChart
   }
}
</script>

<style scoped>

.bg{
      /*background-image: url('../assets/pics/lani.jpg');
      background-repeat:no-repeat;
      background-attachment:fixed;
      background-position:center;
      background-size: cover;*/
      background-color: #336699;
      z-index:-1;
      padding: 20px, 20px;
}
.top-block{
  /*margin-top: 20px;*/
  padding-top: 20px;
  height: 40px;
  width: 100%;
  padding-left: 40px;
  padding-right: 100px;
}
.top-left{
  display: inline-block;
}
.top-right{
  display: inline-block;
}
.favicon{
  height: 20px;
}
.c-mainpage{
  color: #fff;
  text-decoration: none;
  /*border:1px solid #fff;*/
}

.white{
  color: #fff;
}
.display{
  margin: 20px 20px;
  padding: 20px 20px;
}
</style>
