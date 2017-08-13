<template>
  <div id="app">
     <!--<img src="./assets/pics/logo.png">-->
    <!--<router-view></router-view>-->
    <!-- <base-structure></base-structure> -->
    <salary-chart></salary-chart>
    <geo-shanghai></geo-shanghai>
  </div>

</template>

<script>
// import BaseStructure from './components/Structure.vue'
import SalaryChart from './components/SalaryChart.vue'
import GeoShanghai from './components/GeoShanghai.vue'
export default {
//  name: 'app',
  data () {
    return {
      author: 'zhouxin'
    }
  },
  components: {
    SalaryChart,
    GeoShanghai
   }
}
// document.documentElement.style.overflowY = 'hidden'
// document.body.style.overlfow='hidden'
</script>

<style>
/*#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}*/
</style>
