/**
 * Created by zx on 17-8-11.
 */

$(document).ready(function () {
  var displayH = $(window).height()
  // var displayW = $(window).width()

  // console.log(displayW, displayH)
  var a_salary = ''
  var a_require = ''
  var a_loc = ''
  var a_skill = ''
  var a_scale = ''
  $.ajax({
    url: '/offer/api/',
    method: 'GET',
    success: function (data) {
      // console.log(data)
      a_salary = data['salary']
      a_require = data['require']
      a_loc = data['loc']
      a_skill = data['skill']
      a_scale = data['scale']
      // console.log('ss')
      set_salary(a_salary)
      set_salary_line(a_salary)
      set_geo(a_loc)
      set_req(a_skill)
      set_scale(a_scale)
      set_major(a_require)

    }

  })
  $('.bg').css({'height':displayH})

})

function set_salary (a_salary) {
  var sl_dct = a_salary
  // console.log(sl_dct)
  var years = ['1', '1-3', '3-5', '5-10', '10+']
  var cities = ['北京', '上海', '广州', '深圳', '杭州', '苏州', '西安', '成都', '天津', '南京']

  function get_city (ci) {
    // console.log(dct)
    var city_dct = sl_dct[ci]
    var data = []
    for (i in years){
      var lst_year = city_dct[years[i]]
      var dct_c = {}
      dct_c['data'] = lst_year
      data.push(dct_c)
    }
    return data
  }

  function get_options (c) {
      var dt = []
      for (city in c){
        // console.log(c[city])
        var dct_o = {}
        dct_o['title'] = {text: c[city]}
        dct_o['series'] = get_city(c[city])
        // console.log(dct)
        dt.push(dct_o)
      }
      console.log(dt)
      return dt
  }

  var salarychart = echarts.init(document.getElementById('salary'));

          // 指定图表的配置项和数据
          var option = {
            baseOption:{
              title: {
                  text: 'Python职位薪水',
                  // subtext: '工作年限-工作城市'
                  left: 'center'
              },
              tooltip: {
                  trigger: 'item'
              },
              legend: {
                  data:['1年', '1-3年', '3-5年', '5-10年', '10年+'],
                  right: 'right'
              },
              xAxis: {
                  name: '数量'
              },
              yAxis: {

                  name: '月薪',
                  data: ["5K-","5-10K","10-15K","15-20K","20-25K","25-30K",'30K+','面议']
              },
              timeline: {
                  data: ['北京', '上海', '广州', '深圳', '杭州', '苏州', '西安', '成都', '天津', '南京'],
                  axisType: 'category',
                  autoPlay: true
                  // left: 'center',
                  // bottom: -10
                  // rewind: true
              },
              grid:{
                  bottom: 80
              },
              series: [
              {
                  name: '1年',
                  type: 'bar',
                  stack: '1'

              },
              {
                  name: '1-3年',
                  type: 'bar',
                  stack: '1'

              },

                {
                  name: '3-5年',
                  type: 'bar',
                  stack: '1'

              },
                {
                  name: '5-10年',
                  type: 'bar',
                  stack: '1'

              },
                {
                  name: '10年+',
                  type: 'bar',
                  stack: '1'

              }]
            },
            options: get_options(cities)
          };

          // 使用刚指定的配置项和数据显示图表。
          salarychart.setOption(option);
  }

function set_salary_line (a_salary) {

  var s_dct = a_salary
  var cities = ['北京', '上海', '广州', '深圳', '杭州', '苏州', '西安', '成都', '天津', '南京']

  function salaryline_data (dt) {
    var salaryline_data = []
    for (i in cities){
      var sl_dct = {
              type: 'line',
              label: {
                normal: {
                  show: true,
                  formatter: '{a}: {c}'
                }
              }
            }
      sl_dct['name'] = cities[i]
      // sl_dct['stack'] = '总量'
      var year_dct = dt[cities[i]]
      var sl_nums = [0,0,0,0,0,0,0,0]
      for (k in year_dct){
        var sl_lst = year_dct[k]
        for (j in sl_lst){
          sl_nums[j] = sl_nums[j] + sl_lst[j]
        }
      }
      sl_dct['data'] = sl_nums
      console.log(cities[i], sl_nums)
      salaryline_data.push(sl_dct)
    }

    return salaryline_data
  }

  var salaryline = echarts.init(document.getElementById('salary-line'));

  var option = {
     title: {
          text: '各城市薪资分布图'
      },
      tooltip: {
          trigger: 'axis'
      },
      legend: {
          data:cities
      },
      grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
      },
      toolbox: {
          feature: {
              saveAsImage: {}
          }
      },
      xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ["5K-","5-10K","10-15K","15-20K","20-25K","25-30K",'30K+','面议']
      },
      yAxis: {
          type: 'value'
      },
      series: salaryline_data(s_dct)
  }

  salaryline.setOption(option)

}

function set_geo (geo) {

  var geodt = geo['loc']
  var shanghaichart = echarts.init(document.getElementById('shanghaigeo'));

    var option = {
        title: {
          text: '热门城市地区职位分布',
          color: '#fff'
        },
        tooltip: {
            trigger: 'item'
        },
         bmap: {
          // 百度地图中心经纬度
          center: [112.446806, 32.222042],
          // 百度地图缩放
          zoom: 6,
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
          data:['热门城市地区职位分布'],
          textStyle: {
              color: 'black'
          }
        },
        series: [
          {
            name: '热门城市地区职位分布',
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
}

function set_req (reqdt) {

  var keywords = reqdt['keywords']
  var reqchart = echarts.init(document.getElementById('welfare'));

  function skilldt (kw) {

    var skills = []
    for (i in kw){
      var tem_dct = {}
      tem_dct['name'] = kw[i][0]
      tem_dct['value'] = kw[i][1]
      skills.push(tem_dct)

    }

    return skills
  }
  var option = {
    title:{
        text:"Python职位关键词"
        // link:'https://github.com/ecomfe/echarts-wordcloud',
        // subtext: 'data-visual.cn',
        // sublink:'http://data-visual.cn',
    },
    tooltip: {},
    series: [{
        type: 'wordCloud',
        gridSize: 20,
        sizeRange: [20, 100],
        rotationRange: [0, 0],
        shape: 'circle',
        textStyle: {
            normal: {
                color: function() {
                    return 'rgb(' + [
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160),
                        Math.round(Math.random() * 160)
                    ].join(',') + ')';
                }
            },
            emphasis: {
                shadowBlur: 10,
                shadowColor: '#333'
            }
        },
        data: skilldt(keywords)
    }]
};

  reqchart.setOption(option)

}

function set_scale (scale) {
  var scale_dt = scale['scale']
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
     tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    series: [
              {
                  name:'公司规模',
                  type:'pie',
                  data:scale_dt

              }
          ]

  }

  scalechart.setOption(option)
}

function set_major (major) {
  var major_dt = major['require']

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
}