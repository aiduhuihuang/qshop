from django.urls import path,include
from .views import *

urlpatterns = [
    path("index/",index),
    path("login/",login),
]