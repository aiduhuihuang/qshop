from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(PayOrder)
class PayOrderAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id',"order_number","order_date","order_staus","order_total","order_total"]

@admin.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ["id","order_id","goods_id","goods_price","store_id","goods_count","goods_total_price","ordermark"]