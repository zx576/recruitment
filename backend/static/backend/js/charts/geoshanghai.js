/**
 * Created by zx on 17-8-11.
 */

  var geodt = a_loc['loc']
  var shanghaichart = echarts.init(document.getElementById('shanghaigeo'));

    var option = {
        title: {
          text: '上海地区职位分布',
          color: '#fff'
        },
        tooltip: {
            trigger: 'item'
        },
         bmap: {
          // 百度地图中心经纬度
          center: [121.446806, 31.222042],
          // 百度地图缩放
          zoom: 12,
          // 是否开启拖拽缩放，可以只设置 'scale' 或者 'move'
          roam: true,
          // 百度地图的自定义样式，见 http://developer.baidu.com/map/jsdevelop-11.htm
          mapStyle: {}
      },
        // geo: {
        //   map: '上海'
        //
        // },
        legend: {
          orient: 'vertical',
          y: 'bottom',
          x:'right',
          data:['上海地区职位分布'],
          textStyle: {
              color: 'black'
          }
        },
        series: [
          {
            name: '上海地区职位分布',
            type: 'scatter',
            coordinateSystem: 'bmap',
            symbolSize: 10,
            data: geodt,
            label: {
                normal: {
                    formatter: '{b}',
                    position: 'right',
                    show: true
                },
                emphasis: {
                    show: true
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

  shanghaichart.setOption(option);

  // var bmap = shanghaichart.getModel().getComponent('bmap').getBMap();
  // bmap.addControl(new BMap.MapTypeControl());
