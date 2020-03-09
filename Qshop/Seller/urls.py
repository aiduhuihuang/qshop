from django.urls import path,re_path
from .views import *


urlpatterns = [
   # 注册
   path("register/", register),
   # 登录
   path("login/", login),
    #个人中心
    path("person/",person),
   # 用户退出登录
   path("loginout/", loginout),
   path("index/",index),
#子路由
    path("goods_list/",goods_list),
    re_path("goods_list/(?P<page>\d+)/(?P<status>\d+)/",goods_list),
    re_path("goods_status/(?P<id>\d+)/(?P<status>\w+)/",goods_status),
    #修改商品
    re_path("updategoods/(?P<id>\d+)/",updategoods),
    #商品进货
    path("goodsadd/",goodsadd),

    #订单管理
    path("payorders/",payorders),
    re_path("payorders/(?P<status>\d+)/",payorders),

]