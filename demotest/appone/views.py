from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def appone(request):
    return HttpResponse("这是我的第一个子应用")
def about(request):
    return HttpResponse("这是我的第一个子应用的第二个引用")