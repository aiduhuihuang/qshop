from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def index(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        print((password))
       ## 判断用户是否存在
        flag = Users.objects.filter(username=username).exists()
        if flag:
            ## 存在
           ## 不注册
            message = "用户已经存在"
        else:
        ## 不存在
        ## 注册
        ## 保存数据
            Users.objects.create(username=username,password=password)
            message = "注册成功"
    return render(request, "index.html", locals())

def login(request):

    return HttpResponse("登录页面")