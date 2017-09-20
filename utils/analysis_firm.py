# coding = utf-8
# author = zhouxin
# date = 2017.8.12
# description
# 分析 公司信息

import os, django
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recruitment.server_settings")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recruitment.settings")
django.setup()

from collections import Counter
import jieba
import re
import requests

from backend.models import Recruit, Firm
class AnaFirm:

    def __init__(self):

        self.cities = ['北京', '上海', '广州', '深圳', '杭州', '苏州', '西安', '成都', '天津', '南京']
        self.scale = [0, 50, 100, 500, 1000, 5000, 10000, 100000]
        self.invalid_f = [
            '达内', '黑马', '麦子学院', '优才', '渔阳信通'
        ]

    def f_main(self):

        query = Firm.objects.all()

        scale_dct = {}
        ll_dct = {}
        for item in query:

            loc_ = item.firm_place
            loc = loc_.split('-')[0]
            if loc not in self.cities:
                continue

            scale_f = item.firm_scale_from
            scale_t = item.firm_scale_to

            lng = item.firm_lng
            lat = item.firm_lat

            if lng != -1 and lat != -1:

                ll_city = ll_dct.setdefault(loc, [])
                ll_city.append({'value': [lng, lat, 1]})

            token = scale_f
            if scale_t != 100000:
                token = scale_t

            if token != 0:
                for idx in range(1, len(self.scale)):
                    if token < self.scale[idx]:
                        s = str(self.scale[idx-1]) + '-' + str(self.scale[idx])
                        val = scale_dct.setdefault(s, 0)
                        scale_dct[s] = val + 1
                        break

        scale_lst = []
        for k,v in scale_dct.items():
            dct = {}
            dct['name'],dct['value'] = k,v
            scale_lst.append(dct)

        return [scale_lst, ll_dct]


    def show_firms(self):
        query = Firm.objects.all()
        for f in query:
            # 职位
            r = f.recruit_set.all()
            members = []
            for i in r:
                members.append(i.member)
                # if i.member >= 10:
                #     print(i.url)
            members.sort(reverse=True)
            if not members: continue
            if members[0] >= 5:
                print(f.firm_name, members)

    def filter_firms(self):

        query = Firm.objects.filter(is_alive=True)
        count = 0
        for i in query:
            for word in self.invalid_f:
                if word in i.firm_name:
                    print(i.firm_name)
                    i.is_alive = False
                    i.save()
                    count += 1

        print(count)

    # 获取目前已经证实的培训机构
    # 保存至文件
    def _save_fake_c(self):
        req = requests.get('https://blacklist.yitu.yt/companyList/')
        json_dt = req.json()
        res = []
        for item in json_dt['companyList']:
            res.append(item['name'])

        with open('fakeCompany.txt', 'w')as f:
            f.write('\n'.join(res))

    # 遍历数据库内数据
    # 查看是否有公司在黑名单上
    def check_blacklist(self):
        with open('fakeCompany.txt', 'r')as f:
            blacklist = f.read()
        query = Firm.objects.all()
        for item in query:
            name = item.firm_name
            try:
                is_on_blist = re.match(name, blacklist)

                # is_on_blist = name in blacklist
                if is_on_blist:
                    print(name)
                    # continue
                    item.is_alive = False
                    jobs = item.recruit_set.all()
                    for job in jobs:
                        job.is_alive = False
                        job.save()

                    item.save()

            except:
                pass


if __name__ == '__main__':
    a = AnaFirm()
    # r = a.f_main()
    # a.show_firms()
    a.check_blacklist()