from django.db import models

# Create your models here.
ISDELETE_STATUS=((0,"否"),(1,"是"))
GENDER_STATUS=((0,"女"),(1,"男"))
GOODS_STATUS=((0,"在售"),(1,"停售"))
USER_STATUS=((0,"买家"),(1,"卖家"))
SUP_STATUS=((0,"合作"),(1,"终止"))
#用户表
class LoginUser(models.Model):
    name=models.CharField(max_length=20,verbose_name="姓名",null=True,blank=True)
    email=models.EmailField(max_length=20,verbose_name="邮箱",unique=True)
    password=models.CharField(max_length=50,verbose_name="密码")
    phone_num=models.CharField(max_length=11,verbose_name="手机号",null=True,blank=True)
    birthday=models.DateField(verbose_name="出生年月",null=True,blank=True)
    age=models.IntegerField(verbose_name="年龄",null=True,blank=True)
    picture=models.ImageField(upload_to="img",default="img/tx.jpg", verbose_name="个人头像")
    gender=models.IntegerField(default=0,choices=GENDER_STATUS,verbose_name="性别")
    address=models.TextField(verbose_name="址地",null=True,blank=True)
    createtime=models.DateTimeField(auto_now=True,verbose_name="创建时间")
    user_status=models.IntegerField(default=0,choices=USER_STATUS,verbose_name="用户类型")
    isDelete=models.IntegerField(default=0,choices=ISDELETE_STATUS,verbose_name="是否删除") #否代表为没有删除,1代表删除

    class Meta:
        db_table="loginuser"
        verbose_name_plural="用户表"
    def __str__(self):
        return self.email

#商品类型表
class Types(models.Model):
    typename=models.CharField(max_length=32,verbose_name="类型名称")
    typeimg=models.ImageField(upload_to="images",default="images/goods.jpg",verbose_name="类型图片")

    class Meta:
        db_table="types"
        verbose_name_plural="商品类型表"

    def __str__(self):
        return self.typename
#供应商表
class Supplier(models.Model):
    sup_name=models.CharField(max_length=32,verbose_name="供应商名称")
    sup_country=models.CharField(max_length=32,verbose_name="供应商/国籍",null=True,blank=True)
    sup_province=models.CharField(max_length=32,verbose_name="省/州",null=True,blank=True)
    sup_city=models.CharField(max_length=32,verbose_name="市",null=True,blank=True)
    sup_area=models.CharField(max_length=32,verbose_name="区县",null=True,blank=True)
    sup_address=models.TextField(max_length=32,verbose_name="具体地址",null=True,blank=True)
    sup_phone=models.CharField(max_length=11,verbose_name="手机号")
    sup_tel=models.CharField(max_length=15,verbose_name="座机电话",null=True,blank=True)
    sup_email=models.EmailField(verbose_name="邮箱",null=True,blank=True)
    sup_sex=models.IntegerField(choices=GENDER_STATUS,default=0,verbose_name="性别")
    sup_user=models.CharField(max_length=20,verbose_name="联系人")
    sup_status=models.IntegerField(default=0,choices=SUP_STATUS,verbose_name="是否合作")

    class Meta:
        db_table="supplier"
        verbose_name_plural="供应商表"
    def __str__(self):
        return self.sup_name

#商品表
class Goods(models.Model):
    Goods_num=models.CharField(max_length=13,verbose_name="商品编号")#商品条形码13位,不足用填充0
    Goods_name=models.CharField(max_length=32,verbose_name="商品名称")
    Goods_price=models.FloatField(verbose_name="销售单价")
    Goods_count=models.IntegerField(verbose_name="商品数量")
    Goods_location=models.CharField(max_length=32,verbose_name="商品产地",null=True,blank=True)
    Goods_safe_date=models.IntegerField(verbose_name="保质期(天)",null=True,blank=True)
    Goods_pro_date=models.DateField(auto_now=True,verbose_name="生产日期")
    Goods_status=models.IntegerField(default=0,choices=GOODS_STATUS,verbose_name="商品状态")
    Goods_inprice=models.FloatField(verbose_name="成本价")
    Goods_img = models.ImageField(upload_to="img", default="img/tx.jpg", verbose_name="商品图片")
    Goods_des=models.TextField(null=True,blank=True,verbose_name="商品描述")
    Goods_info=models.TextField(null=True,blank=True,verbose_name="详细信息")
    #关联id
    types=models.ForeignKey(to=Types,to_field="id",on_delete=models.CASCADE)#关联商品类型
    user=models.ForeignKey(to=LoginUser,to_field="email",on_delete=models.CASCADE)#关联那个卖家
    supplier=models.ForeignKey(to=Supplier,to_field="id",on_delete=models.CASCADE)#关联的供应商

    class Meta:
        db_table="goods"
        verbose_name_plural="商品表"
        ordering=["-id",]




