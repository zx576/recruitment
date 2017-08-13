# -*- coding: utf-8 -*-
import re
import bs4
import datetime
import json

import scrapy
from scrapy.http import Request
from ..items import FirmItem, CrawlendItem
from ..settings import IS_ONLY_TODAY, KEYWORD

class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawlend.middlewares.UAMiddleWare': 546
        },
        'DOWNLOAD_DELAY': 3

    }
    init_url = 'https://m.lagou.com/search.json?city=%E5%85%A8%E5%9B%BD&positionName={0}&pageNo={1}&pageSize=15'
    pagecount = 0

    def start_requests(self):

        self.pagecount += 1
        url = self.init_url.format(KEYWORD, self.pagecount)
        yield Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):

        json_data = json.loads(response.body_as_unicode())
        items = json_data['content']['data']['page']['result']
        if not items:
            return
        else:
            self.pagecount += 1
            url = self.init_url.format(KEYWORD, self.pagecount)
            yield Request(url, callback=self.parse, dont_filter=True)
        for item in items:

            if IS_ONLY_TODAY and '今天' not in item['createTime']:
                continue

            url = 'https://www.lagou.com/jobs/{}.html'.format(item['positionId'])
            yield Request(url, callback=self.parse_lagou, headers={'Referer': 'https://www.lagou.com/'})


    def parse_lagou(self, response):

        soup = bs4.BeautifulSoup(response.body, 'lxml')

        item = {}
        offer = CrawlendItem()
        firm = FirmItem()
        offer['resource'] = '拉钩'
        offer['url'] = response.url
        # 解析 offer 信息
        soup_jobname = soup.find('div', class_='job-name')
        offer['name'] = soup_jobname.get('title')

        # 编译部分正则
        # 　取月薪
        num_p_1 = re.compile(r'(\d+)k')
        num_p_2 = re.compile(r'\d+')

        # 薪水
        soup_salary = soup.find('span', class_='salary')
        res_salary = re.findall(num_p_1, soup_salary.string)
        res_salary.sort()
        if len(res_salary) == 2:
            offer['salary_from'], offer['salary_to'] = [int(i) * 1000 for i in res_salary]
        else:
            offer['is_negotiable'] = True

        # 地点/经验/学历/

        soup_req = soup.find('dd', class_='job_request').find_all('span', class_=False, text=True)
        # print(soup_req)
        offer['work_place'] = soup_req[0].string.replace('/', '').strip()
        firm['firm_place'] = offer['work_place']

        # 工作经验
        exp = soup_req[1].string
        res_exp = re.findall(num_p_2, exp)
        res_exp.sort()
        if len(res_exp) == 2:
            offer['years_of_work_from'], offer['years_of_work_to'] = res_exp
        elif len(res_exp) == 1:
            if int(res_exp[0]) < 10:
                offer['years_of_work_from'] = int(res_exp[0])
            else:
                offer['years_of_work_to'] = int(res_exp[0])

        # 学历
        deg = soup_req[2].string
        if '本科' in deg:
            offer['degree'] = '3'
        elif '不限' in deg:
            offer['degree'] = '6'
        elif '博士' in deg:
            offer['degree'] = '5'
        elif '研究生' in deg:
            offer['degree'] = '4'
        elif '大专' in deg:
            offer['degree'] = '2'
        elif '高中' in deg:
            offer['degree'] = '1'

        # 职位描述的一部分
        # 在拉钩上有个职位标签项， models中没有对应的 field
        # 将其添加到 description 中
        des_1 = soup.find('ul', class_='position-label').get_text(' ', strip=True)

        # 发布日期
        # 发布日期分几种形式
        # 　标准的日期格式 XXXX-XX-XX
        # 近三天简写 1天前　2天前
        date_p = re.compile(r'\d+-\d+-\d+')
        day_p = re.compile(r'(\d+)天')

        release = soup.find('p', class_='publish_time').string
        today = datetime.date.today()

        date_r_1 = re.match(date_p, release)
        date_r_2 = re.match(day_p, release)
        if date_r_1:
            offer['release'] = datetime.datetime.strptime(date_r_1.group(), "%Y-%m-%d").date()

        elif date_r_2:
            offer['release'] = today - datetime.timedelta(days=int(date_r_2.group(1)))

        else:
            offer['release'] = today

        # 职位诱惑
        soup_tem = soup.find('dd', class_='job-advantage')
        tem = soup_tem.p.string
        offer['temptation'] = ';'.join(tem.split(','))

        # 职位描述
        des = soup.find('dd', class_='job_bt')
        offer['description'] = des_1 + des.get_text(strip=True)

        # 公司地址
        soup_l = soup.find('dd', class_='job-address')
        soup_loc = soup_l.find('input', attrs={'name': 'positionAddress'})
        firm['firm_location'] = soup_loc.get('value')

        # 经度
        soup_lng = soup_l.find('input', attrs={'name': 'positionLng'})
        firm['firm_lng'] = float(soup_lng.get('value'))

        # 纬度
        soup_lat = soup_l.find('input', attrs={'name': 'positionLat'})
        firm['firm_lat'] = float(soup_lat.get('value'))

        # 公司信息
        soup_c = soup.find('dl', class_='job_company')

        # 公司名
        soup_img = soup_c.find('img')['alt']
        soup_h2 = soup_c.find('h2')
        soup_h2.span.clear()
        soup_h2 = soup_h2.get_text(strip=True)
        firm['firm_name'] = soup_img or soup_h2

        # 公司领域/规模/网站
        scale_p_1 = re.compile(r'\d+')
        soup_inf = soup.find('ul', class_='c_feature')
        soup_inf_li = soup_inf.find_all('li')
        for li in soup_inf_li:
            val, key = [i for i in li.stripped_strings]
            if key == '领域':
                firm['firm_industry'] = val
            elif key == '规模':
                res_sca = re.findall(scale_p_1, val)
                if len(res_sca) == 2:
                    res_sca.sort()
                    firm['firm_scale_from'], firm['firm_scale_to'] = res_sca
                elif len(res_sca) == 1:
                    firm['firm_scale_from'] = res_sca[0]

            elif key == '公司主页':
                firm['firm_website'] = val

        item['offer'] = offer
        item['firm'] = firm

        yield item
