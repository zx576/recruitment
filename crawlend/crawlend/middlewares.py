# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import queue
import logging
from scrapy import signals

from .proxies import _Proxy
from .headers import get_header

logger = logging.getLogger(__name__)
class CrawlendSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 更改代理和 UA 中间件
class ProxyMiddleWare():

    '''
    更改代理和UA的中间件
    说明：
     _Proxy() 提供 代理 IP
     get_headers() 提供 UA

     策略：
     初始化提取 20 个 IP 入队，每次请求更换 IP 和 UA,
     response 和 exception 中如果请求失败，则重新发出请求
    如果请求成功，则重新入队该 IP

    当队列中少于 10 个 IP ，则再从 _Proxy 中提取 20

    '''
    def __init__(self):
        self.q = queue.Queue()
        self.p = _Proxy()

    def _enqueue(self):
        proxies = self.p.extract(n=20)
        for i in proxies:
            self.q.put(i)

    # 在请求中植入 UA 和 header
    def process_request(self, request, spider):
        self._check_remain_proxies()
        request.headers.setdefault("User-Agent", get_header()['User-Agent'])
        _proxy = self.q.get()
        request.meta["proxy"] = _proxy[1]
        # 代理索引值
        request.meta["proxy_index"] = _proxy[0]
        request.meta["dont_redirect"] = True

        logger.debug("construct request with proxy: {}".format(request.meta["proxy"]))

    # 遇到问题重新构造请求
    def process_exception(self, request, exception, spider):
        # logger.debug("%s exception: %s" % (request.meta["proxy"], exception))
        # idx = request.meta["proxy_index"]
        # # 删除无效 ip
        # self.p._delete(idx)
        #
        # return self._build_req(request)
        # pass
        pass


    def process_response(self, request, response, spider):

        logger.debug('current response status is {}'.format(response.status))
        # 请求成功
        if response.status == 200:

            addr = request.meta["proxy"]
            self.q.put((request.meta["proxy_index"], addr))
            return response

        else:
            idx = request.meta["proxy_index"]
            # 删除无效 ip
            self.p._delete(idx)
            # 重新植入 UA 和 IP， 发起请求

            return self._build_req(request)

    def _build_req(self, request):

        self._check_remain_proxies()

        # 重新植入 UA 和 IP， 发起请求
        request.headers.setdefault("User-Agent", get_header()['User-Agent'])
        _proxy = self.q.get()
        request.meta["proxy"] = _proxy[1]
        # 代理索引值
        request.meta["proxy_index"] = _proxy[0]
        new_req = request.copy()

        return new_req

    # 检查队列剩余 ip
    # 小于 10 则获取 20 ip 入队
    def _check_remain_proxies(self):

        nums = self.q.qsize()
        if nums < 10:
            self._enqueue()

