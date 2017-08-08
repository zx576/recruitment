# -*- coding: utf-8 -*-

import re
import bs4
import datetime

import scrapy
from scrapy.http import Request
from ..settings import IS_ONLY_TODAY, KEYWORD
from ..items import FirmItem, CrawlendItem

class LiepinSpider(scrapy.Spider):
    name = 'liepin'
    allowed_domains = ['www.liepin.com']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawlend.middlewares.ProxyMiddleWare': None
        },
        'DOWNLOAD_DELAY': 3

    }
    start_urls = []

    if IS_ONLY_TODAY:
        start_urls.append('https://www.liepin.com/zhaopin/?pubTime=1&key={}'.format(KEYWORD))
    else:
        start_urls.append('https://www.liepin.com/zhaopin/?key={}'.format(KEYWORD))

    def parse(self, response):

        soup = bs4.BeautifulSoup(response.body, 'lxml')
        # 下一页
        soup_next = soup.find('a', text='下一页')
        if soup_next:
            next_p = soup_next.get('href')
            if next_p.startswith('http'):
                yield Request(response.url, callback=self.parse, dont_filter=True,
                              headers={'Referer': 'https://www.liepin.com/'})

            # 解析列表
            soup_job_lst = soup.find('ul', class_='sojob-list')
            soup_job_li = soup_job_lst.find_all('li')
            for li in soup_job_li:
                tag_a = li.find('a', attrs={'data-promid': True})
                href = tag_a.get('href')
                if href.startswith('http'):
                    yield Request(href, callback=self.parse_detail, headers={'Referer': 'https://www.liepin.com/'})
        else:
            yield Request(response.url, callback=self.parse, dont_filter=True, headers={'Referer': 'https://www.liepin.com/'})


    def parse_detail(self, responce):

        soup = bs4.BeautifulSoup(responce.body, 'lxml')
        item = {}
        offer = CrawlendItem()
        firm = FirmItem()

        offer['resource'] = '猎聘'
        offer['url'] = responce.url
        # 职位名
        offer['name'] = soup.find('h1').string

        # 职位信息
        soup_div_info = soup.find('div', class_='job-title-left')
        # 薪水
        offer['is_annual_salary'] = True
        salary_p = re.compile(r'(\d+)-(\d+)万')
        soup_salary = soup_div_info.find('p', class_='job-item-title').get_text(strip=True)
        salary_r = re.findall(salary_p, soup_salary)
        if salary_r:
            r = salary_r[0]
            if len(r) == 2:
                offer['salary_from'], offer['salary_to'] = r
            elif len(r) == 1:
                offer['salary_from'] = r[0]

        else:
            offer['is_negotiable'] = True

        # 地址和时间
        soup_basic = soup_div_info.find('p', class_="basic-infor")
        loc, date_ = [i for i in soup_basic.stripped_strings]
        offer['work_place'] = loc
        # 发布时间
        today = datetime.date.today()
        date_p = re.compile(r'\d+-\d+\d+')
        if re.match(date_p, date_):
            offer['release'] = datetime.datetime.strptime(date_, "%Y-%m-%d").date()
        elif '昨天' in date_:
            offer['release'] = today - datetime.timedelta(days=1)
        elif '前天' in date_:
            offer['release'] = today - datetime.timedelta(days=2)
        else:
            offer['release'] = today

        # 其他要求
        soup_qua = soup_div_info.find('div', class_="job-qualifications")
        deg, exp = [i for i in soup_qua.stripped_strings][:2]
        # 学历
        if '本科' in deg:
            offer['degree'] = '3'
        elif '研究生' in deg:
            offer['degree'] = '4'
        elif '博士' in deg:
            offer['degree'] = '5'
        elif '大专' in deg:
            offer['degree'] = '2'
        elif '高中' in deg:
            offer['degree'] = '1'
        else:
            offer['degree'] = '6'
        # 经验
        exp_p = re.compile(r'\d+')
        exp_r = re.findall(exp_p, exp)
        if len(exp_r) == 2:
            offer['years_of_work_from'], offer['years_of_work_to'] = exp_r
        elif len(exp_r) == 1:
            offer['years_of_work_from'] = exp_r[0]

        # 职位诱惑
        soup_y = soup.find('div', class_="tag-list")
        offer['temptation'] = soup_y.get_text(';', strip=True)

        # 职位职责
        soup_div_job = soup.find('div', class_="job-item main-message")
        offer['description'] = soup_div_job.get_text(strip=True)
        # 企业信息
        soup_div_firm = soup.find('div', class_='job-item main-message noborder')
        if soup_div_firm:
            firm['firm_introduction'] = soup_div_firm.get_text(strip=True)

        soup_firm = soup.find('div', class_='company-infor')
        # 公司名
        soup_firm_name = soup_firm.find('a', class_='word')
        firm['firm_name'] = soup_firm_name.get('title')
        # 公司行业, 规模， 性质
        indus, scale, nature = [i for i in soup_firm.ul.stripped_strings][:3]
        firm['firm_industry'] = indus

        # 规模
        scale_p = re.compile(r'\d+')
        scale_r = re.findall(scale_p, scale)
        scale_r.sort()
        if len(scale_r) == 2:
            firm['firm_scale_from'], firm['firm_scale_to'] = scale_r
        elif len(scale_r) == 1:
            firm['firm_scale_from'] = scale_r[0]

        # 性质
        if '外企' in nature:
            firm['firm_nature'] = '2'
        elif '合资' in nature:
            firm['firm_nature'] = '3'
        elif '民营' in nature:
            firm['firm_nature'] = '4'
        elif '国有' in nature:
            firm['firm_nature'] = '1'
        elif '上市' in nature:
            firm['firm_nature'] = '7'

        firm['firm_location'] = soup_firm.p.get_text()

        soup_map = soup.find('div', class_='right-post-map')
        if soup_map:
            soup_loca = soup_map.find('input', attrs={'id': 'location'})
            if ',' in soup_loca.get('value'):
                firm['firm_lng'], firm['firm_lat'] = [float(i) for i in soup_loca.get('value').split(',')]
        item['offer'] = offer
        item['firm'] = firm

        yield item

