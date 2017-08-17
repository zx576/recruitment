/**
 * Created by zx on 17-8-14.
 */
// Python职位主要研究方向

// var major_dt = [{'value': 3721, 'name': '运维'}, {'value': 894, 'name': '后端'}, {'value': 1855, 'name': '数据分析'}, {'value': 749, 'name': '爬虫'}]
var major_dt = a_require['require']

function get_xaxis (dt) {
  var major_x = []
  for (i in major_dt){
    major_x.push(major_dt[i]['name'])

  }
  return major_x
}
var myChart_m = echarts.init(document.getElementById('major'));

  var option = {
        title: {
          text: 'Python职位方向'
        },
        color: ['#3398DB'],
        tooltip : {
            trigger: 'axis',
            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis : [
            {
                type : 'category',
                data : get_xaxis(major_dt),
                axisTick: {
                    alignWithLabel: true
                }
            }
        ],
        yAxis : {
          name: '职位数量'
        },
        series : [
            {
                name:'职位方向',
                type:'bar',
                barWidth: '60%',
                data:major_dt
            }
        ]
    };

myChart_m.setOption(option)