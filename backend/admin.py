from django.contrib import admin
from .models import Recruit, Proxy, Firm


@admin.register(Proxy)
class ProxyAdmin(admin.ModelAdmin):
    list_display = ('head', 'addr', 'is_alive', 'is_http_and_https')
    list_editable = ('is_alive',)
    list_per_page = 50

@admin.register(Recruit)
class RecruitAdmin(admin.ModelAdmin):
    list_display = ('resource', 'name', 'degree', 'release', 'work_place','salary_from', 'salary_to')
    list_filter = ('resource', 'created_time')


@admin.register(Firm)
class FirmAdmin(admin.ModelAdmin):
    list_display = ('firm_name', 'firm_nature', 'firm_industry', 'firm_scale_from', 'firm_scale_to')