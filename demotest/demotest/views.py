from django.http import HttpResponse

def index(request,id,m):
    result=str(m)+"-----"+str(id)
    return HttpResponse("这是一个视图"+result)

from django.shortcuts import render_to_response
def oneindex(request):
    name="Lsss"
    age="18"
    hobby=('python','c++','java')
    params={'name':'Lisi','age':20,'hobby':['唱歌','跳舞']}
    # return render_to_response('oneindex.html',params)
    return render_to_response('oneindex.html', locals())