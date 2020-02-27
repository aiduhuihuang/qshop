from django.shortcuts import render
from django.http import HttpResponse,FileResponse
from django.conf import settings
from django.utils.encoding import escape_uri_path
import os

def upfile(request):
    if request.method=="POST":
        print(request.FILES)
        f=request.FILES["upname"]
        filepath= os.path.join(settings.MEDIA_ROOT,f.name)
        print(filepath)
        with open(filepath,"wb") as fp:
            for info in f.chunks():
                fp.write(info)
        return HttpResponse("长传成功")
    return render(request,"upflie.html")

lisk = []
newlist=[]
def down(request):
    #获取名字
    lisk.clear()
    newlist.clear()
    getAllDir(settings.MEDIA_ROOT)

    for one in  lisk:
        s=os.path.basename(one)
        newlist.append(s)
    return render(request,"down.html",{"files":newlist})

def download(request,id=0):
    print(id)
    the_file_name = settings.MEDIA_ROOT + "\\" + newlist[int(id)-1]
    print(the_file_name)
    file = open(the_file_name, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(escape_uri_path(newlist[int(id)-1]))
    return response


def getAllDir(path):
    fileList=os.listdir(path)
    for filename in fileList:
        fileAbsPath = os.path.join(path,filename)
        if os.path.isdir(fileAbsPath):
            getAllDir(fileAbsPath)
        else:
            lisk.append(fileAbsPath)