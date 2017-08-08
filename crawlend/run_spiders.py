# coding = utf-8
# author = zhouxin
# description
# 启动所有爬虫

import scrapy
from scrapy.cmdline import execute
import multiprocessing

spiders = [
    'scrapy crawl zhilian',
    'scrapy crawl job51'
    'scrapy crawl liepin'
    'scrapy crawl lagou'
]

if __name__ == '__main__':

    processes = []

    for s in spiders:
        p = multiprocessing.Process(target=execute, args=(s.split(),))
        processes.append(p)

    for i in processes:
        i.start()

    for j in processes:
        j.join()





