# coding=utf-8
# author = zhouxin
# date = 2017.8.12
# description
# 分析 backend 中的数据，转换成前端可直接使用的数据
import os, django
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recruitment.settings")
django.setup()

from collections import Counter
import jieba
import re

from backend.models import Recruit, Firm

class AnaRecruit:

    def __init__(self):

        self.cities = ['北京', '上海', '广州', '深圳', '杭州', '苏州', '西安', '成都', '天津', '南京']
        self.tags = []
        self.__require = ''

    def r_main(self):

        r_query = Recruit.objects.all()
        salary_dct = {}


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
            salart_f = item.salary_from
            salart_t = item.salary_to
            is_annual = item.is_annual_salary
            is_neg = item.is_negotiable
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
                        token_1.append(salart_f // 12)
                    else:
                        token_1.append(salart_f)

            elif exp_f != 0 and exp_t != 50:
                token_1.append(str(exp_f))
                token_2.append(str(exp_t))

                if is_neg:
                    token_1.append(-1)
                else:
                    if is_annual:
                        token_1.append(salart_f // 12)
                        token_2.append(salart_t // 12)

                    else:
                        token_1.append(salart_f)
                        token_2.append(salart_t)

            else:
                token_1.append(str(exp_f))
                if is_neg:
                    token_1.append(-1)
                else:
                    if is_annual:
                        token_1.append(salart_f//12)

                    else:
                        token_1.append(salart_f)

            standard = [5000, 10000, 15000, 20000, 25000, 30000, 2**31]

            if len(token_1) == 2:
                # print(token_1)
                # 处理 token 1
                if token_1[0] == '不限' or int(token_1[0]) <= 5:
                    exp_n = city_dct.setdefault(token_1[0], [0 for i in range(7)])
                elif 5 < int(token_1[0]) <= 10:
                    exp_n = city_dct.setdefault('5-10', [0 for i in range(7)])
                elif int(token_1[0]) > 10:
                    exp_n = city_dct.setdefault('10+', [0 for i in range(7)])
                s = token_1[1]

                if s == -1:
                    exp_n[-1] += 1
                for i in range(len(standard)):
                    if s < standard[i]:
                        exp_n[i] += 1

            if len(token_2) == 2:
                # print(token_2)
                # 处理 token 2
                if token_1[0] == '不限' or int(token_1[0]) <= 5:
                    exp_n = city_dct.setdefault(token_1[0], [0 for i in range(7)])
                elif 5 < int(token_1[0]) <= 10:
                    exp_n = city_dct.setdefault('5-10', [0 for i in range(7)])
                elif int(token_1[0]) > 10:
                    exp_n = city_dct.setdefault('10+', [0 for i in range(7)])

                s = token_2[1]
                if s == -1:
                    exp_n[-1] += 1
                for i in range(len(standard)):
                    if s < standard[i]:
                        exp_n[i] += 1
        return salary_dct

    def get_tags(self):

        # 统计职位诱惑词频前 20 位
        c = Counter(self.tags)
        res = c.most_common(20)
        return res

    def get_req(self):

        # # 统计职位要求出现频率前 20
        # text = list(jieba.cut(self.__require))
        # c = Counter(text)
        # res = c.most_common(20)
        # return res

        keywords = ['运维', '后端', '数据分析', '爬虫']

        dct = {}
        for i in keywords:
            p = re.compile(r'{}'.format(i))
            count = len(re.findall(p,self.__require))
            dct[i] = count

        return dct

    



if __name__ == '__main__':

    a = Analysis()
    r = a.r_main()
    print(r)
    r2 = a.get_tags()
    print(r2)
    r3 = a.get_req()
    print(r3)










