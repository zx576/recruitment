<template lang="html">

  <div class="box" id='shanghaigeo' v-bind:style="{height: displayH + 'px', width: displayW + 'px'}">

  </div>

</template>

<script>
export default {
  mounted: function () {
    var echarts = require('echarts');
    var sh = require('../../assets/js/shanghai.js')
    // console.log(sh)

    var myChart = echarts.init(document.getElementById('shanghaigeo'));
    var option = {
        title: {
          text: '上海地区职位分布',
          color: '#fff'
        },
        tooltip: {
            trigger: 'item'
        },
        geo: {
          map: 'shanghai'
        },
        legend: {
          orient: 'vertical',
          y: 'bottom',
          x:'right',
          data:['上海地区分布'],
          textStyle: {
              color: '#fff'
          },
        },
        series: [
          {
            name: '上海地区职位分布',
            type: 'scatter',
            coordinateSystem: 'geo',
            data: [
              {name: [121.76,	31.05], value:1},
              {name: [121.70, 31.19],  value:1},
              {name: [121.48,	31.41], value:1},
            ]
          }
        ]
      }
  myChart.setOption(option);
},
  data () {
    return {
      displayH: (document.documentElement.screenHeight) * 0.6,
      displayW: (document.documentElement.screenWidth) * 0.6
    }
  }
}
</script>

<style lang="css">
</style>
