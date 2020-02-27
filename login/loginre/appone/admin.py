from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    def isDelete(self):
        if self.isDelete:
            return "是"
        else:
            return "否"

    list_display = ["id","username","password","createtime",isDelete]