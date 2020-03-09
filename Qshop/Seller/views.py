from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import *

# Create your views here.

#密码加密
import hashlib
def setpassword(pwd):
    md5=hashlib.md5()
    md5.update(pwd.encode())
    result=md5.hexdigest()
    return result

#登录装饰器
def loginvalid(func):
    def inner(request,*args,**kwargs):
        #根据后台登录设置的
        c_email=request.COOKIES.get("selleremail")
        print(c_email)
        c_status=request.COOKIES.get("sellerstatus")
        print(c_status)
        s_email=request.session.get("selleremail")
        print(s_email)
        s_status=request.session.get("sellerstatus")
        print(s_status)
        if c_email and s_email and c_email==s_email:
            return  func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/seller/login/")#重定向到登录页面
    return  inner

#注册页面
def register(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        repassword=request.POST.get("repassword")
        if email and password and password==repassword:
            params={"email":email,"password":setpassword(repassword),"user_status":1}
            user_obj=LoginUser.objects.create(**params)
            if user_obj:
                return HttpResponseRedirect("/seller/login/")
            else:
                message="用户注册失败"
                return render(request, "seller/register.html", locals())
        else:
            message="都不能为空,且密码两次一样"
            return render(request, "seller/register.html", locals())
    return render(request,"seller/register.html",locals())

#ajax判断用户是否注册(利用ajax去判断用户是否已经注册了)
def ajax_register(request):
    email = request.GET.get("email")
    print("email:"+email)
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
#ajax判断密码两次输入的是否一样
def ajax_pregister(request):
    result = {"code": 10000, "msg": ""}
    password = request.POST.get("password")

    repassword = request.POST.get("repassword")
  # print(request.POST)

    if repassword and password and repassword==password:
         result = {"code": 10000, "msg": ""}
    else:
        result = {"code": 10001, "msg": "密码不为空或两次必须一样"}
    return JsonResponse(result)


#模板页面
@loginvalid
def base(request):
    return render(request, "seller/base.html")
#用户登录
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email and password:
            user_obj=LoginUser.objects.filter(email=email,password=setpassword(password),user_status=1).first()
            if user_obj:
                print(user_obj)
                response=HttpResponseRedirect("/seller/index/")
                response.set_cookie("selleremail",user_obj.email) #把邮件写入cook
                response.set_cookie("sellerimg",str(user_obj.picture)) #把图片写入
                response.set_cookie("sellerstatus",user_obj.user_status) #把状态也写进去
                request.session["selleremail"]=user_obj.email
                request.session["sellerimg"] = str(user_obj.picture)
                request.session["sellerstatus"] = user_obj.user_status
                return response
            else:
                message = "邮箱或密码不正确"
                return render(request, "seller/login.html", locals())
        else:
            message = "邮箱和密码不能为空"
            return render(request, "seller/login.html", locals())
    return render(request, "seller/login.html")

#后台用户退出登录
def loginout(request):
    response=HttpResponseRedirect("/seller/login/")
    response.delete_cookie("selleremail")
    response.delete_cookie("sellerimg")
    response.delete_cookie("sellerstatus")
    del request.session["selleremail"]
    del request.session["sellerimg"]
    del request.session["sellerstatus"]
    return response
#首页
@loginvalid
def index(request):
    picture=request.COOKIES.get("sellerimg")
    print(picture)
    return render(request, "seller/index.html", locals())

#商品信息(路由在子路由LoginUser中)加载商品信息
#分页用到的包
from django.core.paginator import Paginator
@loginvalid
def goods_list(request,status=3,page=1):
    #返回到前端的一个标题值
    goods_title=""
    if status=="0" or status=="1":# 0在售商品,1是停售
        if status=="0":
            goods_title="在售商品"
        else:
            goods_title="停售商品"
        goods_obj=Goods.objects.filter(Goods_status=status).order_by("-id")
    else:
        goods_title="全部商品"
        goods_obj=Goods.objects.all().order_by("-id")
    if goods_obj:
        paginator=Paginator(goods_obj,8)
        page_obj=paginator.page(page)
        print(page_obj)#代表每一页的数据对象
    else:
        message="未找到相关记录"
    return render(request, "seller/goods_list.html", locals())

#商品的上架和下架功能实现,都是修改状态
@loginvalid
def goods_status(request,id,status):
    #找到这个数据
    # print(request.META["HTTP_REFERER"])#获取的是当前页面地址
    goods_obj=Goods.objects.get(id=id)
    if status=="up":#点击上架说明原来是下架的（下架的为1）
        goods_obj.Goods_status=0
        goods_obj.save()
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else: #下架
        goods_obj.Goods_status=1
        goods_obj.save()
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

#修改商品
@loginvalid
def updategoods(request,id):
    #查询所有的供应商信息
    sup_obj=Supplier.objects.all()
    # back_ulr=request.META["HTTP_REFERER"]
    try:
        back_ulr = request.META["HTTP_REFERER"]
    except:
        # back_ulr=request.META["PATH_INFO"]
        # print(request.META["HTTP_HOST"])
        pass
    u_goods_obj=Goods.objects.get(id=id)#获取id对应的商品信息
    #get就是读取数据
    if request.method=="POST":
        # 修改和保存数据
        try:
            u_goods_obj.Goods_num=request.POST.get("goodsnum") #商品编码
            u_goods_obj.Goods_name = request.POST.get("goodsname") #名称
            goodsp = request.POST.get("goodsprice") #销售价
            u_goods_obj.Goods_price=str(goodsp).split("$")[1]
            u_goods_obj.Goods_count = request.POST.get("goodscount") #数量
            u_goods_obj.Goods_pro_date = request.POST.get("goodsdate") #生产日期
            u_goods_obj.Goods_status=request.POST.get("radiostatus") #商品状态
            select_g=request.POST.get("select_g") #供应商
            u_goods_obj.supplier_id=str(select_g).split(":")[0]
            goodsip = request.POST.get("goodsinp") #进价
            u_goods_obj.Goods_inprice=str(goodsip).split("$")[1]
            u_goods_obj.Goods_location = request.POST.get("goodscity") #产地
            u_goods_obj.Goods_safe_date = request.POST.get("goodssafe") #保质期
            u_goods_obj.save()
            message="修改数据成功"#代表数据成功
        except:
            message="修改数据失败"#数据失败
        return render(request, "seller/updategoods.html", locals())
    else:
        if u_goods_obj:
            return render(request, "seller/updategoods.html", locals())
        else:
            return HttpResponseRedirect("没有找到相关数据")



#商品进货
@loginvalid
def goodsadd(request):
    good_titile="商品进货"
    #查出所有类型
    t_obj=Types.objects.all()
    s_obj=Supplier.objects.all()
    if request.method=="POST":
        u_goods_obj=Goods()
        # 修改和保存数据
        try:
            u_goods_obj.Goods_num=request.POST.get("goodsnum") #商品编码
            print( u_goods_obj.Goods_num)
            u_goods_obj.Goods_name = request.POST.get("goodsname") #名称
            print(u_goods_obj.Goods_name)
            goodsp = request.POST.get("goodsprice") #销售价
            u_goods_obj.Goods_price=float(str(goodsp).split("$")[1])
            print(u_goods_obj.Goods_price)
            u_goods_obj.Goods_count = int(request.POST.get("goodscount")) #数量
            print(u_goods_obj.Goods_count)
            u_goods_obj.Goods_pro_date = request.POST.get("goodsdate") #生产日期
            print(u_goods_obj.Goods_pro_date)
            u_goods_obj.Goods_status=int(request.POST.get("radiostatus")) #商品状态
            print(u_goods_obj.Goods_status)
            select_g=request.POST.get("select_g") #供应商
            u_goods_obj.supplier_id=int(str(select_g).split("-")[0])
            print(u_goods_obj.supplier_id)
            select_t=request.POST.get("select_t")
            u_goods_obj.types_id=int(str(select_t).split("-")[0])
            print(u_goods_obj.types_id)
            goodsip = request.POST.get("goodsinp") #进价
            u_goods_obj.Goods_inprice=float(str(goodsip).split("$")[1])
            print(u_goods_obj.Goods_inprice)
            u_goods_obj.Goods_location = request.POST.get("goodscity") #产地
            print(u_goods_obj.Goods_location)
            u_goods_obj.Goods_safe_date = int(request.POST.get("goodssafe")) #保质期
            print(u_goods_obj.Goods_safe_date)
            u_goods_obj.Goods_img=request.FILES.get("filename")
            u_goods_obj.user_id=request.COOKIES.get("selleremail")
            print(u_goods_obj.Goods_img)
            u_goods_obj.save()
            message="增加数据成功"#代表数据成功
        except:
            message="增加数据失败"#数据失败
        return render(request, "seller/goodadd.html", locals())

    return  render(request,"seller/goodadd.html",locals())

#个人中心
@loginvalid
def person(request):
    person_tilet = "个人中心"
    email = request.COOKIES.get("selleremail")
    user_obj = LoginUser.objects.get(email=email)
    if request.method=="POST":
        user_obj.name=request.POST.get("name")
        print("姓名"+user_obj.name)
        if request.POST.get("birthday"):
            user_obj.birthday = request.POST.get("birthday")
        user_obj.phone_num = request.POST.get("tel")
        print("手机号"+user_obj.phone_num)
        if request.POST.get("age"):
            user_obj.age = int(request.POST.get("age"))
        else:
            user_obj.age=0
        user_obj.gender = int(request.POST.get("gender"))
        print(user_obj.gender)
        user_obj.address = request.POST.get("address")
        print(user_obj.address)
        user_obj.createtime = request.POST.get("createtime")
        print(user_obj.createtime)
        if request.POST.get("status"):
            user_obj.user_status = request.POST.get("status")
        if request.FILES.get("img"):
            user_obj.picture = request.FILES.get("img")
            print(user_obj.picture)
        user_obj.save()
        message = "修改数据成功"  # 代表数据成功
        return render(request,"seller/person.html",locals())
    else:
        if email and user_obj:
            print(user_obj.picture)
            return render(request,"seller/person.html",locals())
        else:
            return HttpResponseRedirect("/seller/login/")

#订单信息
def payorders(request,status=0):
    if status=="0":
        order_title="全部订单"
    elif status=="2":
        order_title = "已完成订单"
    elif status=="3":
        order_title = "进行中订单"
    else:
        order_title = "取消的订单"
    return render(request,"seller/payoders.html",locals())
