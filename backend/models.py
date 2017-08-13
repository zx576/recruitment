from django.db import models
import datetime

today = datetime.date.today()

class Recruit(models.Model):

    belong = models.ForeignKey('Firm', verbose_name='所属公司', default='')
    resource = models.CharField('信息来源', max_length=255)
    url = models.URLField('信息链接', default='')
    name = models.CharField('职位名', max_length=255)
    salary_from = models.IntegerField('工资低点', default=0)
    salary_to = models.IntegerField('工资高点', default=0)
    is_annual_salary = models.BooleanField('是否为年薪', default=False)
    is_negotiable = models.BooleanField('是否面议', default=False)

    # 0 表示不要求工作年限
    # 50 表示 3年以上 5年以上的上值
    years_of_work_from = models.IntegerField('工作年限低点', default=0)
    years_of_work_to = models.IntegerField('工作年限高点', default=50)
    work_place = models.CharField('工作地点', max_length=255)
    CHOICES = (
        ('1', '高中及以下'),
        ('2', '大专'),
        ('3', '普通本科'),
        ('4', '研究生'),
        ('5', '博士及以上'),
        ('6', '未知')
    )
    degree = models.CharField('学历要求', choices=CHOICES, max_length=255)

    # 职位诱惑有多个，以分号隔开
    temptation = models.CharField('职位诱惑', max_length=255)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    release = models.DateField('发布日期')
    description = models.TextField('职位描述')
    member = models.IntegerField('招聘人数', default=-1)

    # 其他属性
    is_alive = models.BooleanField('是否有效', default=True)
    created_time = models.DateTimeField('创建日期', auto_now_add=True)
    modified_time = models.DateTimeField('修改日期', auto_now=True)

    # patch
    is_add = models.BooleanField('是否添加', default=False)

    def __str__(self):
        return self.name

class Firm(models.Model):
    # 公司相关信息
    firm_introduction = models.TextField('公司简介')

    # 公司规模默认从 0 开始
    # 100000 表示上限
    firm_name = models.CharField('公司名', max_length=255, default='')
    firm_scale_from = models.IntegerField('公司规模低点', default=0)
    firm_scale_to = models.IntegerField('公司规模高点', default=100000)

    CHOICES2 = (
        ('1', '国企'),
        ('2', '外企'),
        ('3', '合资'),
        ('4', '民营'),
        ('5', '其他'),
        ('6', '股份'),
        ('7', '上市')
    )
    firm_nature = models.CharField('企业性质', choices=CHOICES2, default='5', max_length=255)
    firm_industry = models.CharField('企业行业', max_length=255)
    firm_location = models.CharField('公司地址', max_length=255)
    firm_place = models.CharField('公司省市', max_length=255, default='')

    # 不用 URLField 是因为一些招聘信息中没有此信息
    # 同时给出的地址可能是相对地址
    firm_website = models.CharField('公司网站', default='', max_length=255)
    # 地图位置
    firm_lng = models.FloatField('经度', default=-1)
    firm_lat = models.FloatField('纬度', default=-1)

    # 其他属性
    is_alive = models.BooleanField('是否有效', default=True)
    created_time = models.DateTimeField('创建日期', auto_now_add=True)
    modified_time = models.DateTimeField('修改日期', auto_now=True)

    # patch
    is_add = models.BooleanField('是否添加', default=False)



    def __str__(self):
        return self.firm_name

# 存入一些
class Proxy(models.Model):

    head = models.CharField('代理类型', default='http', max_length=255)
    addr = models.CharField('代理地址', max_length=255)
    is_alive = models.BooleanField('是否有效', default=True)
    is_http_and_https = models.BooleanField('是否包含所有协议', default=False)

    def __str__(self):
        return self.addr
