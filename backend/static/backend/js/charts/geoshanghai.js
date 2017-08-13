/**
 * Created by zx on 17-8-11.
 */


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
          map: '上海'
        },
        legend: {
          orient: 'vertical',
          y: 'bottom',
          x:'right',
          data:['上海地区职位分布'],
          textStyle: {
              color: '#fff'
          }
        },
        series: [
          {
            name: '上海地区职位分布',
            type: 'scatter',
            coordinateSystem: 'geo',
            data: [
              {value: [121.76,	31.05, 1]},
              {value: [121.70, 31.19, 1]},
              {value: [121.48,	31.41, 1]}
            ],
            label: {
                normal: {
                    formatter: '{b}',
                    position: 'right',
                    show: true
                },
                emphasis: {
                    show: false
                }
            },
            itemStyle: {
                normal: {
                    color: 'red'
                }
            }
          }
        ]
      }
  myChart.setOption(option);