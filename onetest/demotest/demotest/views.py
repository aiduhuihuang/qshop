from django.shortcuts import render,render_to_response

def index(request):
    name = "杜辉煌"
    return render(request,"index.html",locals())

def about(request):
    name = "杜辉煌"
    return render_to_response("about.html",locals())

def gbook(request):
    name = "杜辉煌"
    return  render_to_response("gbook.html",locals())


def info(request):
    name="杜辉煌"
    return  render_to_response("info.html",{"name":name})


def list(request):
    name="杜辉煌"
    return  render_to_response("list.html",locals())

def share(request):
    name="杜辉煌"
    return  render_to_response("share.html",locals())