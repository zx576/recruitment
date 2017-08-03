from django.db import models


class Offer(models.Model):

    name = models.CharField('职位名', max_length=255)

# 存入一些
class Proxy(models.Model):

    head = models.CharField('代理类型', default='http', max_length=255)
    addr = models.CharField('代理地址', max_length=255)
    is_alive = models.BooleanField('是否有效', default=True)
    is_http_and_https = models.BooleanField('是否包含所有协议', default=False)

    def __str__(self):
        return self.addr


