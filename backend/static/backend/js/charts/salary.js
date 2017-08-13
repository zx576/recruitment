/**
 * Created by zx on 17-8-11.
 */
var myChart = echarts.init(document.getElementById('salary'));

        // 指定图表的配置项和数据
        var option = {
          baseOption:{
            title: {
                text: 'Python职位薪水',
                subtext: '工作年限-工作城市',
                textStyle: {
                  color: '#fff'
                },
                left: 'center'
            },
            tooltip: {
                trigger: 'item'
            },
            legend: {
                data:['不限', '一年', '三年', '五年'],
                right: 'right'
            },
            xAxis: {
                name: '数量'
            },
            yAxis: {

                name: '月薪',
                data: ["5K","10K","15K","20K","25K","30K"]
            },
            timeline: {
                data: ['北京', '上海', '广州'],
                axisType: 'category',
                autoPlay: true,
                rewind: true,
            },
            series: [{
                name: '不限',
                type: 'bar',
                stack: '1'

            },
            {
                name: '一年',
                type: 'bar',
                stack: '1'

            },
            {
                name: '三年',
                type: 'bar',
                stack: '1'

            },
            {
                name: '五年',
                type: 'pie',

                roseType: false,
                center: ['75%', '25%'],
                radius: [0, '30%']
            }
          ]
          },
          options: [
            {
              title: {text: '北京'},
              series: [
                {data: [5, 20, 36, 10, 10, 20]},
                {data: [5, 20, 36, 10, 10, 20]},
                {data: [5, 20, 36, 10, 10, 20]},
                {
                  data: [
                    {name: 'k', value: 10},
                    {name: 'a', value: 10},
                    {name: 'f', value: 10},
                    {name: 'g', value: 10},
                    {name: 'j', value: 10}
                  ]
                }
              ]
            },
            {
              title: {text: '上海'},
              series: [
                {data: [5, 20, 36, 10, 10, 20]},
                {data: [5, 20, 36, 10, 10, 20]},
                {data: [5, 20, 36, 10, 10, 20]},
                {
                  data: [
                    {name: 'k', value: 10},
                    {name: 'a', value: 10},
                    {name: 'f', value: 10},
                    {name: 'g', value: 10},
                    {name: 'j', value: 10},
                  ],
                }
              ]
            },
            {
              title: {text: '广州'},
              series: [
                {data: [5, 20, 36, 10, 10, 20]},
                {data: [5, 20, 36, 10, 10, 20]},
                {data: [5, 20, 36, 10, 10, 20]},
                {
                  data: [
                    {name: 'k', value: 10},
                    {name: 'a', value: 10},
                    {name: 'f', value: 10},
                    {name: 'g', value: 10},
                    {name: 'j', value: 10}
                  ]
                }
              ]
            }
          ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);