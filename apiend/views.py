from django.shortcuts import render

'''
薪水：

{
    '北京': {
        # 工作年限: [5k薪水数量, 10K薪水数量, ...]
        '不限': [v1, v2, v3, v4, v5, v6]
        }
    '上海': {
        # 工作年限: [5k薪水数量, 10K薪水数量, ...]
        '不限': [v1, v2, v3, v4, v5, v6]
        }
    '广州': {
        # 工作年限: [5k薪水数量, 10K薪水数量, ...]
        '不限': [v1, v2, v3, v4, v5, v6]
        }
}

地理位置

{
    '北京': [
    {value: [lng, lat, count]},
    {value: [lng, lat, count]},
    {value: [lng, lat, count]},
    ],
    
    '上海': [
    {value: [lng, lat, count]},
    {value: [lng, lat, count]},
    {value: [lng, lat, count]},
    ]

}

词云

[
    {'name': xxx, 'value': xxx},
    {'name': xxx, 'value': xxx},
    {'name': xxx, 'value': xxx},
]

公司规模

[
    {name: '0-50', value: 0},
    {name: '0-50', value: 0},
    {name: '0-50', value: 0},
]


'''