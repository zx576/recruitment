# -*- coding: utf-8 -*-
import scrapy
import bs4
from ..items import CrawlendItem

'''
描述:

1. 在项目初期要积累大量的原始数据，所以要不限时间的爬
2. 在项目后期维护阶段，就只爬今日更新的数据
3. 抽象出 bs 处理函数，方便之后更改
'''

class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['https://www.zhaopin.com/']
    # start_urls = ['http://www.zhaopin.com/']
    start_urls = [
            'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E4%B8%8A%E6%B5%B7%3b%E5%8C%97%E4%BA%AC%3b%E5%B9%BF%E5%B7%9E%3b%E6%B7%B1%E5%9C%B3%3b%E6%88%90%E9%83%BD'
                '&kw=python&sb=2&sm=0&isfilter=0&isadv=0&sg=9d2c7faca43c4d7cbe4ad6f47d47212d&p=1',
            ]


    def parse(self, response):
        soup = bs4.BeautifulSoup(response.body, 'lxml')
        # print(soup.find('title').string)
        soup_div = soup.find('div',class_='bottom_t')
        soup_li = soup_div.find_all('a')
        for li in soup_li:
            name = li.string
            item = CrawlendItem()
            item['name'] = name.strip()
            yield item

