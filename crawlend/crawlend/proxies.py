# coding=utf-8
# date=2017.8.2

import requests
from backend.models import Proxy

class _Proxy:

    def __init__(self):
        self.url = 'http://lab.crossincode.com/proxy/get/?num=20'
        self.offset = 0
        self.p = Proxy.objects.filter(is_alive=True)
        self.remain = len(self.p)
        self._check()

    def _check(self):
        if self.remain < 20:
            self._get_proxies()

    # 获取代理
    def _get_proxies(self):

        # 获取 ip
        url = self.url + '&offset={}'.format(self.offset)
        req = requests.get(url)
        raw = req.json()
        for i in raw['proxies']:
            try:
                Proxy.objects.get(addr=i['http'])
            except:
                # 更新个数
                self.remain += 1
                Proxy.objects.create(
                    addr=i['http']
                )

    # 提取 n 个 ip
    # 默认为 1
    def extract(self, n=1):

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
            addr = 'http://{}'.format(next_ip.addr)
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
