<template lang="html">
  <div class="bg-pic-1" v-bind:style="{height: screenHeight + 'px'}">

  </div>

</template>

<script>
export default {
  data () {
    return {
      key: 'zhang',
      screenWidth: document.documentElement.clientWidth,
      screenHeight: document.documentElement.clientHeight
    }
  }

}
</script>

<style scoped>
.bg-pic-1{
  background-image: url('../assets/pics/Preikestolen.jpg');
  background-repeat:no-repeat;
  background-attachment:fixed;
  background-position:center;
  background-size: cover;
}
</style>
