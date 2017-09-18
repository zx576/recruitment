/**
 * Created by zx on 17-8-11.
 */

$(document).ready(function () {
  var displayH = $(window).height()
  if (displayH > 1000){
    $('.bg').css({'min-height':1000})
  } else {
    $('.bg').css({'min-height':displayH})
  }

  // console.log($('.col-md-6').width())
  // var displayW = $(window).width()

  // console.log(displayW, displayH)
  // var displayW = $('.display').width()
  //
  // $('.box').css({'width':displayw, 'height': displayW*(0.6)})
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


})

// timeline
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
      // console.log(dt)
      return dt
  }
  var salary_chart = document.getElementById('salary')
  var wh = myChartContainer(salary_chart);
  var screenw = wh[0];
  var screeh = wh[1];
  var salarychart = echarts.init(salary_chart);

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
            media:[
              // query 1
              {
                query:{
                  maxAspectRatio: 1
                },
                option:{
                  grid:{
                    // left: 'center',
                    top: '100',
                    width: '80%',
                    height: '60%'
                  },
                  legend: {
                    left: '0',
                    top: '5%',
                    orient: 'horizontal'
                  },
                  timeline:{
                    left: '10%',
                    bottom: '8%'
                  }

                }
              },
              //query 2
              {
                query:{
                  minAspectRatio: 1
                },
                option:{
                  grid:{
                    left: 'center',
                    width: '60%',
                    height: '60%'

                  },
                  legend: {
                    right: '20%'
                  },
                  timeline: {
                    bottom: '20%'
                  }
                }
              }
            ],
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
      var year_dct = dt[cities[i]]
      var sl_nums = [0,0,0,0,0,0,0,0]
      for (k in year_dct){
        var sl_lst = year_dct[k]
        for (j in sl_lst){
          sl_nums[j] = sl_nums[j] + sl_lst[j]
        }
      }
      sl_dct['data'] = sl_nums
      salaryline_data.push(sl_dct)

    }

    // console.log(salaryline_data)
    return salaryline_data
  }

  var salary_line = document.getElementById('salary-line')
  myChartContainer(salary_line)
  var salaryline = echarts.init(salary_line);

  var option = {
     baseOption:{
       title: {
          text: '各城市薪资分布图',
         left: 'center'
      },
      tooltip: {
          trigger: 'axis'
      },
      legend: {
          data:cities,
          top: '7%'
      },
      grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
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
     },
      media: [
        {
          query:{
            maxAspectRatio: 1
          },
          option:{
            grid:{
                // left: 'center',
                top: '100',
                width: '90%',
                height: '60%'
              },
            legend:{
              top: '5%'
            },
            dataZoom: [
                {
                    id: 'dataZoomX',
                    type: 'slider',
                    xAxisIndex: [0],
                    filterMode: 'filter',
                    start: 0,
                    end: 30,
                    bottom: '15%'
                }
            ]
          }
        },
        {
          query:{
            minAspectRatio: 1
          },
          option:{
            grid:{
              top: 100,
              left:'center',
              width: '60%',
              height: '60%'
            }
          }
        }
      ]

  }

  salaryline.setOption(option)

}

function set_geo (geo) {

  var geodt = geo['loc']
  // var shanghaichart = echarts.init(document.getElementById('shanghaigeo'));
  var shanghai_chart = document.getElementById('shanghaigeo')
  myChartContainer(shanghai_chart)
  var shanghaichart = echarts.init(shanghai_chart);

    var option = {
        title: {
          text: '热门城市地区职位分布',
          color: '#fff'
        },
        tooltip: {
            trigger: 'item'
        },
        // grid:{
        //   width: '60%',
        //   height: '60%'
        // },
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
        legend: {
          orient: 'vertical',
          y: 'bottom',
          x:'right',
          data:['热门城市地区职位分布'],
          textStyle: {
              color: 'black'
          }
        },
        // media:[
        //   {
        //     query:{},
        //     option:{}
        //   }
        // ],
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

  var keys = get_keys()
  var req_chart = document.getElementById('welfare')
  myChartContainer(req_chart)
  var reqchart = echarts.init(req_chart);

  var prefix = {
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
        }
    }

  var base_series_data = get_base_series(keys)
  var options_series_data = get_series(keys)



  function get_keys () {
    var k = []
    for (i in reqdt){
      k.push(i)
    }

    return k
  }
  function get_base_series (keys) {

    var s = []
    for (i in keys){
      s.push(prefix)
    }

    return s
  }

  function get_series (keys) {

    var series = []
    for (i in keys){
      var items = reqdt[keys[i]]
      var pf = {
        title: {
          'text': keys[i]
        }
      }
      var kvs = []
      for (j in items){
        var tem = {}
        tem['name'] = items[j][0]
        tem['value'] = items[j][1]
        kvs.push(tem)
      }
      pf['series'] = []
      pf['series'].push({'data': kvs})
      series.push(pf)
    }

    return series
  }



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

  // console.log(keys)
  var option = {
    baseOption: {
      title:{
          text:"Python职位关键词",
          left:'center'
      },
      timeline: {
        data: keys,
        autoPlay: true,
        // playInterval: 1000,
        axisType: 'category'
      },
      series: base_series_data
      },
    options: options_series_data,
    media: [
      {
        query:{
          maxAspectRatio: 1
        },
        option:{
          timeline:{
            left: 0
          },
          grid:{
            width: '100%',
            height: '100%',
            left: 0
          }
        }
      }
    ]
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

  // var scalechart = echarts.init(document.getElementById('scale'));
  var scale_chart = document.getElementById('scale')
  myChartContainer(scale_chart)
  var scalechart = echarts.init(scale_chart);

  var option = {

    baseOption: {
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
    },
    media: [
      {
        query: {
          minAspectRatio: 1
        },
         grid: {
            left: 'center',
            width: '60%',
            height: '60%'
          }
      }
    ]

  }

  scalechart.setOption(option)
}

function set_major (major) {
  var major_dt = major
  // ....
  // var major_dt = {'运维': [1656, 27383506, 3811], 'web': [1833, 30331159, 4087], '深度学习': [235, 5455734, 451], '游戏': [130, 1531494, 170], '数据分析': [1089, 22611427, 2323], '爬虫': [223, 4097155, 427]}


  // ....
  function get_xaxis () {
    var major_x = []
    for (i in major_dt){
      major_x.push(i)

    }
    return major_x
  }
  // 职位数量
  function get_recuit (dt) {
    var nums = []
    for (i in dt){
      nums.push(major_dt[dt[i]][0])
    }
    return nums
  }
  // 职位平均薪水
  function get_average (dt) {
    var avg = []
    for (i in dt){
      var total = major_dt[dt[i]][1]
      var count = major_dt[dt[i]][0]
      avg.push(Math.ceil(total/count))
    }
    return avg
  }
  function get_years (dt) {
    var avgy = []
    for (i in dt){
      var total_y = major_dt[dt[i]][2]
      var count = major_dt[dt[i]][0]
      avgy.push((total_y/count).toFixed(2))

    }
    return avgy
  }
  var xaxis = get_xaxis()
  var recruit_nums = get_recuit(xaxis)
  var avg_salary = get_average(xaxis)
  var avg_year = get_years(xaxis)
  var r_max = Math.max.apply(null, recruit_nums)
  var a_max = Math.max.apply(null, avg_salary)
  var y_max = Math.max.apply(null, avg_year)

  var myChartm = document.getElementById('major')
  myChartContainer(myChartm)
  var myChart_m = echarts.init(myChartm);

  var option = {
        baseOption:{
          title: {
          text: 'Python职位'
        },
        // color: ['#3398DB'],
        tooltip : {
            trigger: 'axis',
            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        legend: {
            data: ['职位方向','职位平均月薪', '职位平均年限']
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
                data : xaxis,
                axisTick: {
                    alignWithLabel: true
                }
            }
        ],
        yAxis :[{
            type: 'value',
            name: '职位数量',
            min: 0,
            max: r_max,
            position: 'left',
            axisLabel: {formatter: '{value} 个'}
        }, {
            type: 'value',
            name: '职位平均月薪',
            min: 5000,
            max: a_max,
            position: 'right',
            axisLabel: {formatter: '{value} 元'}
        },
        {
            type: 'value',
            name: '职位平均工作年限',
            min: 0,
            max: y_max,
            position: 'right',
            offset: 100,
            axisLabel: {formatter: '{value} 年'}
        }],
          series : [
            {
                name:'职位方向',
                type:'bar',
                barWidth: '60%',
                yAxisIndex: 0,
                data:recruit_nums
            },
            {
              name:'职位平均月薪',
              type: 'line',
              yAxisIndex: 1,
              data: avg_salary
            },
            {
              name:'职位平均年限',
              type: 'line',
              yAxisIndex: 2,
              data: avg_year

            }
        ]
        },
        media: [
          {
            query: {
              minAspectRatio: 1
            },
            option: {
              grid: {
                left: 'center',
                width: '60%',
                height: '60%'
              }
            }
          },
          {
            query: {
              maxAspectRatio: 1
            },
            option: {
              grid: {
                // left: 'center',
                width: '120%',
                height: '60%',
                top: 100
              },
              title: {
                left: 'center'
              },
              legend:{
                top: '5%'
              },
              yAxis :[{
                  type: 'value',
                  name: '职位数量',
                  min: 0,
                  max: r_max,
                  position: 'left',
                  axisLabel: {formatter: '{value} 个'}
              }, {
                  show: false
              },
              {
                 show: false
              }]

            }
          }
        ]
    };

myChart_m.setOption(option)
}

var myChartContainer = function (myChart) {

    var screenW = window.innerWidth;
    var screenH = window.innerHeight;
    myChart.style.width =  screenW*(0.9)+'px';
    myChart.style.height = screenH*(0.9) +'px';

    return [screenW, screenH]
};



