# coding=utf-8
# date=2017.8.2

import requests
from backend.models import Proxy

class _Proxy:

    def __init__(self):
        self.url = 'http://lab.crossincode.com/proxy/get/?num=20'
        self.offset = 0
        self.offset_https = 0
        self.p = Proxy.objects.filter(is_alive=True)
        self.p_https = self.p.filter(head='https')
        self.remain = len(self.p)
        self.remain_https = len(self.p_https)
        self._check()

    def _check(self):
        if self.remain < 20:
            self._get_proxies()
        if self.remain_https < 3:
            self._get_proxies(is_https=True)

    # 获取代理
    def _get_proxies(self, is_https=False):

        # 获取 ip
        if is_https:
            url = self.url + '&offset={0}&head=https'.format(self.offset_https)
        else:
            url = self.url + '&offset={}'.format(self.offset)
        req = requests.get(url)
        raw = req.json()
        for i in raw['proxies']:
            try:
                Proxy.objects.get(addr=i['http'])
            except:
                # 更新个数
                self.remain += 1
                if is_https:
                    Proxy.objects.create(
                        addr=i['https'],
                        head='https'

                    )
                else:
                    Proxy.objects.create(
                        addr=i['http']

                    )

    # 提取 n 个 ip
    # 默认为 1
    def extract(self, n=1, is_https=False):

        if is_https:
            if self.remain_https < 3:
                self.offset_https += 10
                self._get_proxies(is_https=True)
            proxies = iter(self.p_https)
            n = n if 0 < n < self.remain_https else self.remain_https
        else:
            # 检查剩余 ip
            if self.remain <= 20:
                self.offset += 20
                self._get_proxies()
            proxies = iter(self.p)
            n = n if 0 < n < self.remain else self.remain

        lst = []
        count = 0
        while True:
            if count == n:
                break
            next_ip = next(proxies)
            addr = '{0}://{1}'.format(next_ip.head, next_ip.addr)
            proxy = (next_ip.id, addr)
            lst.append(proxy)
            count += 1

        return lst

    # 删除某个 ip
    def _delete(self, id):

        query = Proxy.objects.get(pk=id)
        query.is_alive = False
        query.save()
        self.remain -= 1
