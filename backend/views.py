from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Proxy, Recruit, Firm, ShapedData
import datetime
import json


def index(request):
    return render(request, 'backend/base.html', {'key': 'value'})


@csrf_exempt
def proxy_list(request):

    if request.method == 'GET':

        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)

        try:
            dt = ShapedData.objects.latest('created_time')
        except:
            dt = ShapedData.objects.all()[::-1][0]

        dct = {}
        dct['salary'] = json.loads(dt.salary)
        dct['require'] = json.loads(dt.require)
        dct['skill'] = json.loads(dt.skill)
        dct['scale'] = json.loads(dt.scale)
        dct['loc'] = json.loads(dt.location)
        # print(dct)
        return JsonResponse(dct, safe=False)



