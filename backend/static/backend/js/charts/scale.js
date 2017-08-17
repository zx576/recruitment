/**
 * Created by zx on 17-8-14.
 */
// 公司规模 饼图

var scale_dt = [{'name': '100-500', 'value': 988}, {'name': '500-1000', 'value': 458}, {'name': '1000-5000', 'value': 164}, {'name': '0-50', 'value': 121}, {'name': '5000-10000', 'value': 264}, {'name': '50-100', 'value': 871}, {'name': '10000-100000', 'value': 102}]
function scale_get_x (dt) {
  var scale_x = []
  for (i in dt){
    scale_x.push(dt[i]['name'])
  }
  return scale_x
}

var scalechart = echarts.init(document.getElementById('scale'));

var option = {
  title: {
    text: '招聘 Python 公司规模'
  },
  series: [
            {
                name:'公司规模',
                type:'pie',
                data:scale_dt,
                itemStyle:{
                  normal:{
                    color: '#000'
                  },
                  
                }
            }
        ]

}

scalechart.setOption(option)