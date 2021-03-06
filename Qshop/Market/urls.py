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
   #立即购买订单
   path("place_order/",placeorder),
   #用户中心
   path("user_center_info/",user_center_info),
   #用户全部订单
   path("user_center_order/",user_center_order),
   #用户地址
   path("user_center_site/",user_center_site),
   #退出
   path("loginout/",loginout),

   #提交订单后到付款页面
   path("alipay_order/",alipay_order),

   #回调处理结果
   path("payresult/",pay_result),
   path("add_cart/",add_cart),
   #删除购物数据
   path("delete_cart/",delete_cart),



]