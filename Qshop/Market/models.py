from django.db import models
from Seller.models import LoginUser,Goods

# Create your models here.

ORDER_STATUS = (
    (1,"未支付"),
    (2,"已支付"),
    (3,"待发货"),
    (4,"已发货"),
    (5,"拒收"),
    (6,"已完成"),
)
ISCHECKED=((1,"是"),(0,"否"))
class PayOrder(models.Model):
    order_number = models.CharField(max_length=40,unique=True,verbose_name="订单号")
    order_date = models.DateField(auto_now=True,verbose_name="订单创建时间")
    order_staus = models.IntegerField(choices=ORDER_STATUS,verbose_name="订单状态")
    order_total = models.FloatField(verbose_name="订单总价")
    order_user = models.ForeignKey(to=LoginUser,to_field="email",on_delete=models.CASCADE,verbose_name="买家")
    class Meta: 
        db_table = "pay_order"
        verbose_name_plural="订单表"

class OrderInfo(models.Model):
    order = models.ForeignKey(to=PayOrder,on_delete=models.CASCADE,verbose_name="订单ID")
    goods = models.ForeignKey(to=Goods,on_delete=models.CASCADE,verbose_name="商品ID")
    goods_price = models.FloatField(verbose_name="商品的单价")
    store = models.ForeignKey(to=LoginUser,to_field="email",on_delete=models.CASCADE,verbose_name="卖家邮箱")
    goods_count = models.IntegerField(verbose_name="购买的单品的数量")
    goods_total_price = models.FloatField(verbose_name="购买的单品的总金额")
    ordermark=models.TextField(null=True,blank=True,verbose_name="备注信息")
    class Meta:
        db_table = "order_info"
        verbose_name_plural="订单详情表"

class Cart(models.Model):
    goods = models.ForeignKey(to=Goods,on_delete=models.CASCADE)
    goods_number = models.IntegerField(verbose_name="商品的数量")
    goods_total = models.FloatField(verbose_name="商品的小计")
    # goods_price = models.FloatField()
    cart_user = models.ForeignKey(to=LoginUser,to_field="email",on_delete=models.CASCADE,verbose_name="买家")
    class Meta:
        db_table = "cart"
        verbose_name_plural="购物车表"


#卖家地址模型（loginuser表中的USER_STATUS=0）
class UserAddress(models.Model):
    uname=models.CharField(max_length=32,verbose_name="姓名")
    addinfo=models.CharField(max_length=60,verbose_name="详细地址")
    yinfo=models.CharField(max_length=10,verbose_name="邮编")
    tel=models.CharField(max_length=11,verbose_name="电话号码")
    ischecked=models.IntegerField(choices=ISCHECKED,verbose_name="是否默认")
    user=models.ForeignKey(to=LoginUser,to_field="email",on_delete=models.CASCADE,verbose_name="买家")
    class Meta:
        db_table="Useraddress"
        verbose_name_plural="详细地址表"
