from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from Seller.models import *
from .models import *
from Seller.views import setpassword
from django.core.paginator import Paginator

# Create your views here.
#登录装饰器
def loginvalid(func):
    def inner(request,*args,**kwargs):
        #根据后台登录设置的
        c_email=request.COOKIES.get("maketemail")

        s_email=request.session.get("maketemail")
        if c_email and s_email and c_email==s_email:
            return  func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/maket/login/")#重定向到登录页面
    return  inner

#注册
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
        u_pwd=request.POST.get("pwd")
        user_obj=LoginUser.objects.filter(email=u_name,password=setpassword(u_pwd),user_status=0).first()
        if user_obj:
            name = user_obj.name
            response=HttpResponseRedirect("/maket/index/")
            response.set_cookie("maketemail",u_name)
            response.set_cookie("status",user_obj.user_status)
            request.session["maketemail"]=u_name
            request.session["status"]=user_obj.user_status
            return response
        else:
            message="用户名或密码不正确"
            return render(request,"maket/login.html",locals())
    else:
        return render(request,"maket/login.html")

#退出
@loginvalid
def loginout(request):
    response = HttpResponse("")
    response.delete_cookie("maketemail")
    response.delete_cookie("status")
    del request.session["maketemail"]
    del request.session["status"]
    return response

#首页
@loginvalid
def index(request):
    email=request.COOKIES.get("maketemail")
    user_obj=LoginUser.objects.filter(email=email,user_status=0).first()
    #查询类型
    type_obj=Types.objects.all()
    return render(request,"maket/index.html",locals())

#订单详情
@loginvalid
def detail(request,id):
    g_obj=Goods.objects.get(id=id)
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

#商品列表
@loginvalid
def list(request,id,page=1):#用post方法来区别搜索商品
    if request.method=="POST":
        goods_search=request.POST.get("search")
        good_obj=Goods.objects.filter(Goods_name__icontains=goods_search).all()
    else:
        good_obj=Goods.objects.filter(types_id=id).order_by("Goods_pro_date").all()
    if good_obj:
        paginator = Paginator(good_obj, 10)
        page_obj = paginator.page(page)
        new_goods=good_obj[:2]
    return render(request,"maket/list.html",locals())

#立即购买
import uuid
@loginvalid
def placeorder(request):
    v=10
    #获取传过来的值
    nums=request.GET.get("nums")
    id=request.GET.get("goodsid")
    email=request.COOKIES.get("maketemail")
    # 商品信息
    goods_obj = Goods.objects.get(id=id)
    order_obj = PayOrder()
    #如果商品id和卖家一样 都存在说明买的是同一个订单中的商品 且是未支付
    oinfo_obj = OrderInfo.objects.filter(goods=goods_obj,store_id=goods_obj.user_id).first()
    #判断合并条件是否符合
    if oinfo_obj and oinfo_obj.order.order_staus==1:
        #修改商品
        oinfo_obj.goods_count = int(oinfo_obj.goods_count)+int(nums)
        oinfo_obj.store_id=goods_obj.user_id #卖家
        oinfo_obj.goods_total_price=float(oinfo_obj.goods_total_price)+float(goods_obj.Goods_price)*int(nums)
        oinfo_obj.save()
        #修改订单
        order_obj=PayOrder.objects.filter(id=oinfo_obj.order_id).first()
        order_obj.order_total=oinfo_obj.goods_total_price
        order_obj.save()
    else:
        #生成订单
        order_obj.order_number="".join(str(uuid.uuid4()).split("-"))
        print(order_obj.order_number)
        order_obj.order_staus=1
        order_obj.order_total=float(goods_obj.Goods_price)*int(nums)
        print(order_obj.order_total)
        order_obj.order_user_id=email #买家id
        print(order_obj.order_user)
        order_obj.save()#保存
        #生成订单详细信息
        oinfo_obj=OrderInfo()
        oinfo_obj.order=order_obj
        print(oinfo_obj.order)
        oinfo_obj.goods=goods_obj
        print(oinfo_obj.goods)
        oinfo_obj.goods_price=goods_obj.Goods_price
        oinfo_obj.store=goods_obj.user
        print(oinfo_obj.store)
        oinfo_obj.goods_count=int(nums)
        oinfo_obj.goods_total_price=order_obj.order_total
        oinfo_obj.ordermark=""
        oinfo_obj.save()
    return render(request,"maket/place_order.html",locals())

#支付宝付款码的生成
from Qshop.settings import alipay
def alipay_order(request):
    pay_id=request.GET.get("pay_id")
    print(pay_id)
    pay_obj=PayOrder.objects.get(id=int(pay_id))
    if pay_obj:
        #实例一个订单
        order_string = alipay.api_alipay_trade_page_pay(
            subject="食品交易",  ## 主题
            out_trade_no=pay_obj.order_number,  ## 订单号
            total_amount=str(pay_obj.order_total),  ## 交易金额   字符串
            return_url="http://127.0.0.1:8000/maket/payresult/",  ##  回调的地址
            notify_url=None  ## 通知
        )
    #返回支付宝url
        result="https://openapi.alipaydev.com/gateway.do?"+order_string
        return  HttpResponseRedirect(result)
    else:
        return HttpResponseRedirect("/maket/index/")

#接受支付宝的回调地址处理结果
## 接收支付宝的支付结果
def pay_result(request):
    out_trade_no = request.GET.get("out_trade_no")
    ## 修改订单的状态  未付款 -》 已付款
    if out_trade_no:
        p_obj = PayOrder.objects.get(order_number=out_trade_no)
        p_obj.order_staus=2  #修改订单状态
        p_obj.save()
        return render(request,"maket/payresult.html",locals())

#用户中心
def user_center_info(request):

    return render(request,"maket/user_center_info.html")

#用户订单数据
def user_center_order(request):

    return  render(request,"maket/user_center_order.html")

#购物车#找到属于自己的购物车
def cart(request):
    user_obj=LoginUser.objects.filter(email=request.COOKIES.get("maketemail")).first()
    total={"yunfei":10,"totalcount":0,"totalmoney":0}
    c_obj=Cart.objects.filter(cart_user=user_obj).all()
    #取值运费和总数量和总的金额以及统计商品类型,数量总数
    if c_obj:
        for i in c_obj:
            total["totalcount"]+=int(i.goods_number)
            total["totalmoney"]+=float(i.goods_total)
    return render(request,"maket/cart.html",locals())

#增加购物车数据
def add_cart(request):
    #数据格式
    result={"code":10000,"msg":"添加商品成功","goods_name":""}
    goods_id=request.POST.get("goods_id")
    goods_count=request.POST.get("goods_count")
    goods_money=request.POST.get("goods_money")
    status=request.POST.get("status")
    user_email=request.COOKIES.get("maketemail")
    #根据商品id查询商品信息
    g_obj=Goods.objects.filter(id=goods_id).first()
    l_obj=LoginUser.objects.filter(email=user_email).first()
    if g_obj:
        #查询是否已经存在在购物车里面了,存在就修改，不存在就增加
        cart=Cart.objects.filter(cart_user=l_obj,goods=g_obj).first()
        if cart:
            if status=="1":
                cart.goods_number=goods_count
                print(goods_count)
                cart.goods_total=goods_money
                print(goods_money)
            else:
                cart.goods_number +=1
                cart.goods_total=int(cart.goods_number)*float(g_obj.Goods_price)
            cart.save()
        else:
            cart=Cart()
            cart.goods= g_obj
            cart.goods_number = goods_count
            cart.goods_total=g_obj.Goods_price
            cart.cart_user = l_obj
            cart.save()
        result["goods_name"]=g_obj.Goods_name
        print(result)
    return JsonResponse(result)