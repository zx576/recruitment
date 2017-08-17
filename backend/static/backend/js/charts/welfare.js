/**
 * Created by zx on 17-8-11.
 */

var mychart = echarts.init(document.getElementById('welfare'));

  var option = {
    title:{
        text:"PythonZ职位福利"
        // link:'https://github.com/ecomfe/echarts-wordcloud',
        // subtext: 'data-visual.cn',
        // sublink:'http://data-visual.cn',
    },
    tooltip: {},
    series: [{
        type: 'wordCloud',
        gridSize: 20,
        sizeRange: [12, 50],
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
        data: [{'value': 5137, 'name': '五险一金'}, {'value': 3437, 'name': '带薪年假'}, {'value': 3242, 'name': '绩效奖金'}, {'value': 2714, 'name': '定期体检'}, {'value': 2258, 'name': '弹性工作'}, {'value': 1716, 'name': '年底双薪'}, {'value': 1619, 'name': '发展空间大'}, {'value': 1450, 'name': '领导好'}, {'value': 1435, 'name': '岗位晋升'}, {'value': 1381, 'name': '节日礼物'}, {'value': 1320, 'name': '节日福利'}, {'value': 1203, 'name': '员工旅游'}, {'value': 1185, 'name': '午餐补助'}, {'value': 1142, 'name': '扁平管理'}, {'value': 1091, 'name': '交通补助'}, {'value': 1076, 'name': '团队聚餐'}, {'value': 1075, 'name': '技能培训'}, {'value': 971, 'name': '股票期权'}, {'value': 874, 'name': '年度旅游'}, {'value': 843, 'name': '餐补'}]
    }]
};

  mychart.setOption(option)
