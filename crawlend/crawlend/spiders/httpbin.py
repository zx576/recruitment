# -*- coding: utf-8 -*-

'''
本文件为测试用
测试 代理 ip 中间件
测试 django-scrapy 存储
'''
import scrapy
import bs4

from ..items import ProxyItem

class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['www.whatismyip.com.tw']
    start_urls = [
        # 'http://www.whatismyip.com.tw/',
        'https://httpbin.org/ip'
                  ]
    # for i in range(3):
    #     start_urls.append('http://www.whatismyip.com.tw/')

    def parse(self, response):

        soup = bs4.BeautifulSoup(response.body, 'lxml')
        # res = soup.find('b').string
        print(soup)
        item = ProxyItem()

        # item['addr'] = '222.222.222.222'

        yield item
