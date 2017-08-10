from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'api/', views.proxy_list, name='proxy')
]

urlpatterns += format_suffix_patterns(urlpatterns)

