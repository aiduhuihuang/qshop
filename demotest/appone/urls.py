from django.contrib import admin
from django.urls import path,re_path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("index/",appone),
    path("about/",about)
]
