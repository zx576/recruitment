# -*- coding: utf-8 -*-
import scrapy


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['www.whatismyip.com.tw']
    start_urls = ['http://www.whatismyip.com.tw/']

    def parse(self, response):
        pass
