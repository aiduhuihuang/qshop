from django.db import models

# Create your models here.
class Users(models.Model):
    username=models.CharField(max_length=20,verbose_name="登录名")
    password=models.CharField(max_length=20,verbose_name="密码")
    createtime=models.DateTimeField(auto_now=True,verbose_name="创建时间")
    isDelete=models.IntegerField(default=0,verbose_name="是否删除") #否代表为没有删除,1代表删除

    class Meta:
        db_table="users"
        verbose_name_plural="用户表"