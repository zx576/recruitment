# -*- coding: utf-8 -*-
import re
import datetime

import scrapy
from scrapy.http import Request
import bs4

from ..items import CrawlendItem, FirmItem
from ..settings import IS_ONLY_TODAY, KEYWORD

'''
描述:

1. 在项目初期要积累大量的原始数据，所以要不限时间的爬
2. 在项目后期维护阶段，就只爬今日更新的数据
3. 抽象出 bs 处理函数，方便之后更改
'''

class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['https://www.zhaopin.com/']
    # start_urls = ['http://www.zhaopin.com/']
    # 10 个城市
    #　北上广深杭　西安　成都　天津　南京　苏州
    start_urls = []

    all_url =[
                'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8C%97%E4%BA%AC%2B%E4%B8%8A%E6%B5%B7%2B%E5%B9%BF%E5%B7%9E%2B%E6%B7%B1%E5%9C%B3%2B%E6%9D%AD%E5%B7%9E&kw={}&sm=0&p=1&isfilter=0&isadv=0&sb=2',
                'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E8%A5%BF%E5%AE%89%3B%E6%88%90%E9%83%BD%3B%E8%8B%8F%E5%B7%9E%3B%E5%A4%A9%E6%B4%A5%3B%E5%8D%97%E4%BA%AC&kw={}&sm=0&p=1&isfilter=0&isadv=0&sb=2',

            ]

    today_url = [
        'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8C%97%E4%BA%AC%2b%E4%B8%8A%E6%B5%B7%2b%E5%B9%BF%E5%B7%9E%2b%E6%B7%B1%E5%9C%B3%2b%E6%9D%AD%E5%B7%9E&kw={}&sm=0&isadv=0&sb=2&isfilter=1&pd=1&p=1',
        'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E8%A5%BF%E5%AE%89%3B%E6%88%90%E9%83%BD%3B%E8%8B%8F%E5%B7%9E%3B%E5%A4%A9%E6%B4%A5%3B%E5%8D%97%E4%BA%AC&kw={}&sm=0&isadv=0&sb=2&isfilter=1&p=1&pd=1'

    ]

    if IS_ONLY_TODAY:
        for i in today_url:
            start_urls.append(i.format(KEYWORD))

    else:
        for i in all_url:
            start_urls.append(i.format(KEYWORD))

    # 解析招聘信息网页
    def parse(self, response):

        soup = bs4.BeautifulSoup(response.body, 'lxml')
        next_page = soup.find('a', class_='next-page')
        href = next_page.get('href', None)
        # if href:
        #     yield scrapy.Request(href, callback=self.parse)

        soup_tr = soup.find_all('tr', class_=False, style=False)
        for tr in soup_tr[1:]:
            tag_a = tr.find('a')
            href = tag_a.get('href', None)
            if href.startswith('http'):
                yield Request(href, callback=self.parse_detail, dont_filter=True)


    def parse_detail(self, response):

        soup = bs4.BeautifulSoup(response.body, 'lxml')
        item = {}
        offer = CrawlendItem()
        firm = FirmItem()
        offer['resource'] = '智联'
        offer['url'] = response.url
        # 职位 诱惑福利
        # 同时查看该响应是否正确
        soup_div_1 = soup.find('div', class_='inner-left fl')

        if soup_div_1 is None:
            yield Request(response.url, callback=self.parse_detail, dont_filter=True)
            return

        offer['name'] = soup_div_1.h1.string
        offer['temptation'] = soup_div_1.find('div', class_='welfare-tab-box').get_text(';', strip=True)
        # 职位信息
        soup_div_info = soup.find('div', class_='terminalpage-left')
        # soup_li_1 = soup_div_info.find_all('li')
        soup_li_1 = soup_div_info.ul.find_all('li', class_=False)
        # 一些匹配 pattern
        # 薪水
        salary_pattern = re.compile(r'\d+')
        # 发布日期
        day1 = re.compile(r'昨天')
        day2 = re.compile(r'前天')
        day3 = re.compile(r'15天')
        date1 = re.compile(r'\d+-\d+-\d+')

        # 工作经验
        exp = re.compile(r'\d+')

        # 学历
        deg1 = re.compile('博士')
        deg2 = re.compile('研究生')
        deg3 = re.compile('本科')
        deg4 = re.compile('大专')
        deg5 = re.compile('高中')
        deg6 = re.compile('不限')

        for i in soup_li_1:

            key = i.span.get_text(strip=True)
            val = i.strong.get_text()

            if key == '职位月薪：':
                salary = re.findall(salary_pattern, val)
                salary.sort()
                if len(salary) == 2:
                    offer['salary_from'], offer['salary_to'] = salary
                else:
                    offer['is_negotiable'] = True

            elif key == '工作地点：':
                offer['work_place'] = val

            elif key == '发布日期：':

                today = datetime.date.today()
                # 正常的日期 2017-8-3
                res = re.findall(date1, val)
                res1 = re.match(day1, val)
                res2 = re.match(day2, val)
                res3 = re.match(day3, val)
                if len(res) > 0:
                    offer['release'] = datetime.datetime.strptime(res[0], "%Y-%m-%d").date()

                elif res1:
                    offer['release'] = today - datetime.timedelta(days=1)

                elif res2:
                    offer['release'] = today - datetime.timedelta(days=2)

                elif res3:
                    offer['release'] = today - datetime.timedelta(days=15)

                else:
                    offer['release'] = today

            elif key == '工作经验：':

                exprience = re.findall(exp, val)
                exprience.sort()
                if len(exprience) == 2:
                    offer['years_of_work_from'], offer['years_of_work_to'] = exprience

                elif len(exprience) == 1:
                    offer['years_of_work_from'] = exprience[0]

            elif key == '最低学历：':

                degree1 = re.match(deg1, val)
                degree2 = re.match(deg2, val)
                degree3 = re.match(deg3, val)
                degree4 = re.match(deg4, val)
                degree5 = re.match(deg5, val)
                degree6 = re.match(deg6, val)
                if degree1:
                    offer['degree'] = '5'
                elif degree2:
                    offer['degree'] = '4'
                elif degree3:
                    offer['degree'] = '3'
                elif degree4:
                    offer['degree'] = '2'
                elif degree5:
                    offer['degree'] = '1'
                elif degree6:
                    offer['degree'] = '6'

            elif key == '招聘人数：':

                members = re.findall(exp, val)
                if members:
                    offer['member'] = members[0]

        # 包含了 职位描述 和工作地点
        soup_div_2 = soup.find('div', class_="tab-inner-cont", style=False)

        soup_div_2.find('h2').clear()
        soup_div_2.find('b').clear()

        offer['description'] = soup_div_2.get_text(strip=True)
        # firm['firm_location'] = soup_div_2.h2.string.strip()

        # 公司信息
        soup_div_3 = soup.find('div', attrs={'style': 'display:none;word-wrap:break-word;'})
        instruction = soup_div_3.get_text(strip=True)
        firm['firm_introduction'] = instruction
        soup_ul_1 = soup.find('ul', class_='terminal-ul clearfix terminal-company mt20')
        soup_li_2 = soup_ul_1.find_all('li')
        # 公司规模
        scale_p = re.compile(r'\d+')
        # 公司性质

        for li in soup_li_2:
            key = li.span.string.strip()
            val = li.strong.get_text(strip=True)

            if key == '公司规模：':
                res = re.findall(scale_p, val)
                res.sort()
                if len(res) == 2:
                    firm['firm_scale_from'], firm['firm_scale_to'] = res
                elif len(res) == 1:
                    firm['firm_scale_from'] = res[0]
            elif key == '公司性质：':

                if val.startswith('国企'):
                    firm['firm_nature'] = '1'

                elif val.startswith('外商'):
                    firm['firm_nature'] = '2'

                elif val.startswith('合资'):
                    firm['firm_nature'] = '3'

                elif val.startswith('民营'):
                    firm['firm_nature'] = '4'

                elif val.startswith('股份'):
                    firm['firm_nature'] = '6'

                elif val.startswith('上市'):
                    firm['firm_nature'] = '7'

                else:
                    firm['firm_nature'] = '5'

            elif key == '公司行业：':
                firm['firm_industry'] = val

            elif key == '公司主页：':
                firm['firm_website'] = val

            elif key == '公司地址：':
                firm['firm_location'] = val

        soup_firm = soup.find('p', class_="company-name-t")
        firm['firm_name'] = soup_firm.get_text(strip=True)
        item['offer'] = offer
        item['firm'] = firm

        yield item

