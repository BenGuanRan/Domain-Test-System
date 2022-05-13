from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import  ConnetTest

# Create your views here.

def home(request):
    ConnetTest.objects.create(name="阿然", age=20 )
    return HttpResponse('欢迎来到后端主页！')