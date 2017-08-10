<template lang="html">
  <div class="bg-pic" v-bind:style="{height: screenHeight + 'px'}">
    <p>{{ val }}</p>

  </div>
  <!--<img src="../assets/pics/lani.jpg" alt="a">-->
</template>

<script>

export default {

  // console.log('ssss')
  mounted: function(){
    console.log($( document ).width())
    var that = this
    $.ajax({
      url: domain + 'offer/api',
      method: 'GET',
      success: function(data){
        console.log(data)
        that.val = data
      }
    })
  },
  data () {
    return {
      key: 'zhang',
      screenWidth: document.documentElement.clientWidth,
      screenHeight: document.documentElement.clientHeight,
      val: ''
    }
  },



}
</script>

<style scoped>

.bg-pic{

    background-image: url('../assets/pics/lani.jpg');
    background-repeat:no-repeat;
    background-attachment:fixed;
    background-position:center;
    background-size: cover;
}

</style>
