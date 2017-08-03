from django.contrib import admin
from .models import Offer, Proxy

admin.site.register(Offer)


@admin.register(Proxy)
class ProxyAdmin(admin.ModelAdmin):
    list_display = ('head', 'addr', 'is_alive', 'is_http_and_https')
    list_editable = ('is_alive',)
    list_per_page = 50