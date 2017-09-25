# coding = utf-8
# author = zhouxin
# description
# 启动所有爬虫

# import scrapy
from scrapy.cmdline import execute

spiders = [
    'scrapy crawl zhilian',
    'scrapy crawl job51',
    'scrapy crawl liepin',
    'scrapy crawl lagou'
]

if __name__ == '__main__':
    for i in spiders:

        execute(i.split())





