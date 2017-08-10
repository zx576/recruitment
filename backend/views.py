from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Proxy, Recruit, Firm
from .serializers import ProxySerializer


def index(request):
    return render(request, 'index.html', {'key': 'value'})

@csrf_exempt
def proxy_list(request):

    if request.method == 'GET':

        proxies = Proxy.objects.filter(head='http')
        # print(proxies)
        ser = ProxySerializer(proxies, many=True)

        return JsonResponse(ser.data, safe=False)



