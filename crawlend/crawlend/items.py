# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

'''
引入 scrapy_djangoitem 包作为 django-scrapy 存储中介

'''

import scrapy
from scrapy_djangoitem import DjangoItem
from backend.models import Recruit, Firm, Proxy


class CrawlendItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = Recruit

class FirmItem(DjangoItem):
    django_model = Firm

class ProxyItem(DjangoItem):
    django_model = Proxy

