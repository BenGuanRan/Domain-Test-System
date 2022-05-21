from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import  ConnetTest
from .utils.search import  run_one,multifind
import json

# Create your views here.

def home(request):
    ConnetTest.objects.create(name="阿然", age=20 )
    return HttpResponse('欢迎来到后端主页！')

def getSignalInfo(request):
    if request.method == 'GET':
        domain = request.GET.get('domain', default='baidu.com')
        type = request.GET.get('type', default='1')
        res = run_one(domain, type)
        print(res)
        return HttpResponse(json.dumps(res))
    else:
        return  HttpResponse('只支持get')

def getMultipleInfo(request):
    domainlist = ["www.baidu.com", "www.sohu.com", "www.qq.com", "www.hteacher.net", "www.leiphone.com", "www.126.com"]
    res = multifind(domainlist)
    print(res)
    return HttpResponse(json.dumps(res))
