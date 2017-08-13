# coding=utf-8
# author = zhouxin
# date = 2017.8.12
# description
# 根据公司的地址，获取其所在的经纬度

import os, django
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recruitment.server_settings")
django.setup()

import requests
from backend.models import Firm


class LngLat:

    def __init__(self):

        self.domain = 'http://restapi.amap.com/v3/geocode/geo?'
        self.key = '7393f73a51c44149dc5d742aea0013dd'

    # 请求某一个地址
    def _gaode_api(self, addr):

        url = self.domain + 'key=' + self.key + '&address=' + addr
        req = requests.get(url)
        data = req.json()
        geocode = data['geocodes']
        if geocode:
            lnglat = geocode[0]['location']
            lng, lat = [float(i) for i in lnglat.split(',')]
            return [lng,lat]

    def gaode_api(self):

        query = Firm.objects.filter(firm_lat=-1)
        count = 0
        for item in query:
            if count == 1950:
                break
            count += 1
            # 没有确定的地点(猎头代发)
            if not item.firm_location:
                continue

            addr = item.firm_place + item.firm_location
            res = self._gaode_api(addr)
            if res:
                # print(res)
                item.firm_lng, item.firm_lat = res
                item.save()


if __name__ == '__main__':

    l = LngLat()
    l.gaode_api()
