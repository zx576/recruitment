# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import CrawlendItem, FirmItem, ProxyItem
from backend.models import Proxy, Firm, Recruit

# Offer_keys = ['resource', 'url', 'name', 'salary_from', 'salary_to']
class CrawlendPipeline(object):

    def process_item(self, item, spider):
        '''
        :param item: dict
        :param spider:
        :return:

        本项目比较得意的地方，完美解决 django-scrapy 存外键的问题
        在 spider 中使用一个字典存两个 DjangoItem 对象
        在 pipline 中分发两个 DjangoItem 对象
        这样就可以轻松存外键了， 详细说明见博客园：
        '''
        def _check_firm(firm_name):
            try:
                ins = Firm.objects.get(firm_name=firm_name)
                return ins
            except:
                return None
        #
        if isinstance(item, dict):

            # 提取 两个 ITEM
            offer = item['offer']
            firm = item['firm']
            f_name = firm['firm_name']
            offers_ = 0
            # 判断该公司是否存在
            if _check_firm(f_name):
                firm = _check_firm(f_name)
                offers_ = len(firm.recruit_set.filter(name=offer['name']))

            # 保存数据
            firm.save()

            # 判断职位是否有重复
            if offers_ == 0:
                offer['belong'] = Firm.objects.get(firm_name=f_name)
                offer.save()

            return item

        # 测试用
        if isinstance(item, ProxyItem):
            # item.save()
            return item
