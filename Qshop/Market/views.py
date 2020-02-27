from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from Seller.models import *
from Seller.views import setpassword
from django.core.paginator import Paginator

# Create your views here.
def register(request):
    if request.method=="POST":
        user_obj=LoginUser()
        user_name=request.POST.get("user_name")
        email=request.POST.get("email")
        cpwd=request.POST.get("cpwd")
        pwd=request.POST.get("pwd")
        if user_name and cpwd and pwd and cpwd == pwd:
            user_obj.name = user_name
            user_obj.email = email
            user_obj.password = setpassword(cpwd)
            user_obj.user_status = 0
            user_obj.save()
            return render(request,"maket/login.html")
        else:
            message = "用户不为空且两次密码输入要一致"
            return render(request, "maket/register.html", locals())
    else:

        return render(request,"maket/register.html")

#ajax判断邮箱是否已经注册
def ajax_register(request):
    # ajax判断用户是否注册(利用ajax去判断用户是否已经注册了)
    email = request.GET.get("email")
    print("email:" + email)
    if email:
        flag = LoginUser.objects.filter(email=email).exists()
        if flag:
            ## True  账号存在
            message = "邮箱已注册，请换一个"
        else:
            ## flase  账号不存在
            # message = "账号不存在"
            message = ""
    else:
        message = "邮箱不能为空"
    return HttpResponse(message)
#登录
def login(request):
    if request.method=="POST":
        u_name=request.POST.get("username")
        print(u_name)
        u_pwd=request.POST.get("pwd")
        print(setpassword(u_pwd))
        user_obj=LoginUser.objects.filter(email=u_name,password=setpassword(u_pwd),user_status=0).first()
        print(user_obj)
        if user_obj:
            name = user_obj.name
            response=HttpResponseRedirect("/maket/index/")
            response.set_cookie("email",u_name)
            response.set_cookie("status",user_obj.user_status)
            request.session["email"]=u_name
            request.session["status"]=user_obj.user_status
            return response
        else:
            message="用户名或密码不正确"
            return render(request,"maket/login.html",locals())
    else:
        return render(request,"maket/login.html")

#首页
def index(request):
    email=request.COOKIES.get("email")
    user_obj=LoginUser.objects.filter(email=email,user_status=0).first()
    print(user_obj)
    #查询类型
    type_obj=Types.objects.all()
    print(type_obj)
    return render(request,"maket/index.html",locals())


def cart(request):

    return render(request,"maket/cart.html")

def detail(request,id):
    g_obj=Goods.objects.get(id=id)
    print(g_obj)
    new_obj=Goods.objects.filter(types_id=g_obj.types_id).order_by("Goods_pro_date").all()[:2]
    return  render(request,"maket/detail.html",locals())
#ajax产品详细信息求和
def ajax_add(request):
    result={"total":1,"t_price":0}
    c_num=request.GET.get("nums")
    oprcie=request.GET.get("price")
    price=str(oprcie).split("￥")[0]
    total=int(c_num)+1
    t_prcie=str(total*float(price))
    result={"total":total,"t_price":t_prcie}
    return JsonResponse(result)
#ajax减法
def ajax_redius(request):
    result = {"total": 1, "t_price": 0}
    c_num = request.GET.get("nums")
    print(c_num)
    oprcie = request.GET.get("price")
    price = str(oprcie).split("￥")[0]
    print(price)
    if int(c_num)<=1:
        total=1
    else:
        total = int(c_num) - 1
    t_prcie = str(total * float(price))
    print(t_prcie)
    result = {"total": total, "t_price": t_prcie}
    return JsonResponse(result)
def list(request,id,page=1):
    print(id)
    good_obj=Goods.objects.filter(types_id=id).order_by("Goods_pro_date").all()
    if good_obj:
        paginator = Paginator(good_obj, 10)
        page_obj = paginator.page(page)
        new_goods=good_obj[:2]
    return render(request,"maket/list.html",locals())