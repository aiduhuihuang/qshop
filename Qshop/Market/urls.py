from django.urls import path,re_path
from .views import *


urlpatterns = [
   # 前台
   path("register/", register),
   #ajax判断邮箱是否存在
   path("ajax_register/",ajax_register),

   # 登录
   path("login/", login),
   #首页
   path("index/",index),

   #购物车
   path("cart/",cart),

   #更多商品列表
   re_path("list/(?P<id>\d+)/(?P<page>\d+)",list),
   #订单详情
   re_path("detail/(?P<id>\d+)/",detail),
   path("ajax_add/",ajax_add),
   path("ajax_redius/",ajax_redius),



]