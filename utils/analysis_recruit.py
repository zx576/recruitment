# coding=utf-8
# author = zhouxin
# date = 2017.8.12
# description
# 分析 backend 中的数据，转换成前端可直接使用的数据
import os, django
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recruitment.server_settings")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recruitment.settings")
django.setup()

from collections import Counter
import json
import re

from backend.models import Recruit, Firm, ShapedData

class AnaRecruit:

    def __init__(self):

        self.cities = ['北京', '上海', '广州', '深圳', '杭州', '苏州', '西安', '成都', '天津', '南京']
        self.tags = []
        self.__require = ''
        self.exclude = ['and', 'the', 'with','for', 'data',
                        'team', 'work', 'etl', 'good', 'years',
                        'etc', 'will', 'plus', 'from', 'new', 'our',
                        'div', 'are'
                        ]
        self.scale = [0, 50, 100, 500, 1000, 5000, 10000, 100000]

    def r_main(self):

        r_query = Recruit.objects.filter(is_alive=True) #filter(work_place='北京')
        salary_dct = {}

        count = 0
        for item in r_query:

            work_place = item.work_place
            wp = work_place.split('-')[0]
            # 跳过空字符和非城市字符（四川省）
            if wp == '' or len(wp) == 3:
                continue
            if wp not in self.cities:
                continue

            city_dct = salary_dct.setdefault(wp, {})
            exp_f = item.years_of_work_from
            exp_t = item.years_of_work_to

            if exp_f > exp_t:
                exp_f, exp_t = exp_t, exp_f

            salart_f = item.salary_from
            salart_t = item.salary_to

            if salart_f > salart_t:
                salart_f, salart_t = salart_t, salart_f
            is_annual = item.is_annual_salary
            is_neg = item.is_negotiable
            if is_neg:
                count += 1
            # 经验标记
            token_1 = []
            token_2 = []

            # 职位诱惑
            tags_ = item.temptation.split(';')
            self.tags += tags_

            # 职位要求
            self.__require += item.description

            # 经验不限
            if exp_f == 0 and exp_t == 50:
                # exp_0 = city_dct.setdefault('不限', [0 for i in range(7)])
                token_1.append('不限')
                # 薪资面议
                if is_neg:
                    token_1.append(-1)
                else:
                    # 算年薪
                    if is_annual:
                        # token_1.append(salart_f // 12)
                        # token_1.append(salart_t * 10000 // 12)
                        token_1.append((salart_f+salart_t) * 5000 // 12)
                    else:
                        # token_1.append(salart_f)
                        # token_1.append(salart_t)
                        token_1.append((salart_f + salart_t) // 2)

            elif exp_f != 0 and exp_t != 50:
                token_1.append(exp_f)
                token_2.append(exp_t)

                if is_neg:
                    token_1.append(-1)
                    token_2.append(-1)
                else:
                    if is_annual:
                        token_1.append(salart_f * 10000 // 12)
                        token_2.append(salart_t * 10000 // 12)

                    else:
                        token_1.append(salart_f)
                        token_2.append(salart_t)

            elif exp_f != 0 and exp_t == 50:
                token_1.append(exp_f)
                if is_neg:
                    token_1.append(-1)
                else:
                    if is_annual:
                        # token_1.append(salart_f // 12)
                        # token_1.append(salart_t * 10000 // 12)
                        token_1.append((salart_f + salart_t) * 5000 // 12)
                    else:
                        # token_1.append(salart_f)
                        # token_1.append(salart_t)
                        token_1.append((salart_f + salart_t) // 2)

            standard = [5000, 10000, 15000, 20000, 25000, 30000, 2**31]


            if token_1:

                # 第一档
                # 经验不限或者一年
                exp_t1 = token_1[0]

                # print(type(exp_t1), exp_t1)
                if exp_t1 == '不限' or exp_t1 == 1:
                    exp_lst = city_dct.setdefault('1', [0 for i in range(8)])
                elif 1 < exp_t1 <= 3:
                    exp_lst = city_dct.setdefault('1-3', [0 for i in range(8)])
                elif 3 < exp_t1 <= 5:
                    exp_lst = city_dct.setdefault('3-5', [0 for i in range(8)])
                elif 5 < exp_t1 <= 10:
                    exp_lst = city_dct.setdefault('5-10', [0 for i in range(8)])
                else:
                    exp_lst = city_dct.setdefault('10+', [0 for i in range(8)])

                s = token_1[1]
                # 如果是面议
                if is_neg:
                    exp_lst[-1] += 1
                else:
                    for i in range(len(standard)):
                        if s < standard[i]:
                            exp_lst[i] += 1
                            break

            if token_2:
                # 第一档
                # 经验不限或者一年
                exp_t1 = token_2[0]
                if exp_t1 == '不限' or exp_t1 == 1:
                    exp_lst = city_dct.setdefault('1', [0 for i in range(8)])
                elif 1 < exp_t1 <= 3:
                    exp_lst = city_dct.setdefault('1-3', [0 for i in range(8)])
                elif 3 < exp_t1 <= 5:
                    exp_lst = city_dct.setdefault('3-5', [0 for i in range(8)])
                elif 5 < exp_t1 <= 10:
                    exp_lst = city_dct.setdefault('5-10', [0 for i in range(8)])
                else:
                    exp_lst = city_dct.setdefault('10+', [0 for i in range(8)])

                s = token_2[1]
                # 如果是面议
                if is_neg:
                    exp_lst[-1] += 1
                else:
                    for i in range(len(standard)):
                        if s < standard[i]:
                            exp_lst[i] += 1
                            break
        # print(count)
        return salary_dct

    def f_main(self):

        query = Firm.objects.filter(is_alive=True)

        scale_dct = {}
        ll_city = []
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

                # ll_city = ll_dct.setdefault(loc, [])
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

        s = {}
        s['scale'] = scale_lst

        l = {}
        l['loc'] = ll_city

        return [s, l]

    def get_tags(self):

        # 统计职位诱惑词频前 20 位
        c = Counter(self.tags)
        res = c.most_common(20)
        lst = []
        for item in res:
            dct = {}
            dct['name'], dct['value'] = item
            lst.append(dct)
        return lst

    def get_req(self):

        # # 统计职位要求出现频率前 20
        # text = list(jieba.cut(self.__require))
        # c = Counter(text)
        # res = c.most_common(20)

        keywords = ['运维|监控',
                    'web|后端|后台|服务端|django|flask|网络开发|tornado',
                    '数据分析|大数据|hadoop|spark',
                    '爬虫|挖掘|抓取',
                    '游戏|手游',
                    '深度学习|识别|机器学习|神经网络'
                    ]
        lst = []
        for i in keywords:
            dct = {}
            p = re.compile(r'{}'.format(i))
            count = len(re.findall(p,self.__require.lower()))
            dct['value'] = count
            dct['name'] = i.split('|')[0]
            lst.append(dct)

        d = {}
        d['require'] = lst

        return d

    def get_keywords(self):

        pt = re.compile(r'[a-zA-Z]+')
        res = re.findall(pt, self.__require.lower())
        c = Counter([i for i in res if len(i) > 2 and not i in self.exclude])
        lst = c.most_common(80)

        r = []
        for i in lst:
            # print(i[0])
            if i[0] not in self.exclude:
                r.append(i)

        d = {}
        d['keywords'] = r
        return d

    def get_s_keywords(self):

        def match_(desc):
            keywords = ['运维|监控',
                        'web|后端|后台|服务端|django|flask|网络开发|tornado',
                        '数据分析|大数据|hadoop|spark',
                        '爬虫|挖掘|抓取',
                        '游戏|手游',
                        '深度学习|识别|机器学习|神经网络'
                        ]
            for i in keywords:
                p = re.compile(r'{}'.format(i))
                if re.findall(p, desc.lower()):
                    return i.split('|')[0]

        def extract_(desc):
            pt = re.compile(r'[\u4e00-\u9fa5a-z]+')
            rs = re.findall(pt, desc)
            return ''.join(rs)

        def analysis_(content):
            pt = re.compile(r'[a-zA-Z]+')
            res = re.findall(pt, content.lower())
            c = Counter([i for i in res if len(i) > 2 and not i in self.exclude])
            lst = c.most_common(40)
            return lst

        query = Recruit.objects.filter(is_alive=True)
        resdct = {}
        for item in query:
            title = item.name
            description = item.description.lower()
            direction = match_(description+title)
            if not direction:
                continue

            r = resdct.setdefault(direction, '')
            r += description+title
            resdct[direction] = r

        jieba_dct = {}
        for k,v in resdct.items():

            tem = jieba_dct.setdefault(k, [])
            jieba_dct[k] += analysis_(v)



        # jieba_dct = {}
        # for k,v in resdct.items():
        #     r = jieba.cut(v)
        #     c = Counter(r)
        #     c_ = c.most_common(100)
        #     tem = jieba_dct.setdefault(k, [])
        #     tem += c_
        #
        # for i,j in jieba_dct.items():
        #     print(i, j)

        # print(jieba_dct)
        return jieba_dct


    def main(self):


        salary = self.r_main()
        require = self.get_req()
        skill = self.get_keywords()
        scale, ll = self.f_main()
        skill2 = self.get_s_keywords()
        skill2['all'] = skill['keywords']


        # print(salary)
        # print(require)
        # print(skill2)
        # print(scale)
        # print(ll)

        ShapedData.objects.create(
             salary=json.dumps(salary),
             skill=json.dumps(skill2),
             require=json.dumps(require),
             scale=json.dumps(scale),
             location=json.dumps(ll)
         )


    # def show
if __name__ == '__main__':

    a = AnaRecruit()
    a.main()
    # a.get_s_keywords()










