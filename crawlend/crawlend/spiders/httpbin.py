# -*- coding: utf-8 -*-
import scrapy
import bs4

class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['www.whatismyip.com.tw']
    start_urls = ['http://www.whatismyip.com.tw/']
    for i in range(3):
        start_urls.append('http://www.whatismyip.com.tw/')


    def parse(self, response):
        soup = bs4.BeautifulSoup(response.body, 'lxml')
        res = soup.find('b').string
        print(res)

