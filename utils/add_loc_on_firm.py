# coding=utf-8
# author = zhouxin
# date = 2017.8.12
# description
# 根据 Recruit 中的职位信息的工作地点，补充 Firm 中的地理位置信息

import os, django
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recruitment.server_settings")
django.setup()

from backend.models import Recruit, Firm

def add_loc():

    query = Recruit.objects.filter(is_add=True)
    for item in query:

        work_place = item.work_place
        belong = item.belong

        # 职位地点和外键同时存在
        if belong and work_place:
            # 外键的地点不存在
            if belong.firm_place == '':
                belong.firm_place = work_place
                belong.is_add = True
                belong.save()

        # item.is_add = True
        item.save()


if __name__ == '__main__':
    add_loc()
