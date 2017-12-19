from django.shortcuts import render,redirect,HttpResponse

from django.http import QueryDict

from app03 import models
from django.forms import ModelForm

HOST_LIST=[]

for i in range(1500):
    HOST_LIST.append("这是第%s行数据,兄弟们都不要着急哈，慢慢看！"%i)

from components.pager import Pagination


def hosts(request):
    pager_obj = Pagination(request.GET.get('page', 1), len(HOST_LIST), request.path_info, request.GET)
    host_list = HOST_LIST[pager_obj.start:pager_obj.end]

    html = pager_obj.page_html()

    list_condition = request.GET.urlencode()
    params = QueryDict(mutable=True)
    params['_list_filter'] = request.GET.urlencode()
    list_condition = params.urlencode()

    return render(request, 'hosts.html', {'host_list': host_list, "page_html": html, 'list_condition': list_condition})

USER_LIST = []

# for i in range(1,302):
#     USER_LIST.append("bb%s" %i )


def users(request):
    pager_obj = Pagination(request.GET.get('page', 1), len(HOST_LIST), request.path_info, request.GET)
    user_list = HOST_LIST[pager_obj.start:pager_obj.end]

    html = pager_obj.page_html()


    return render(request, 'users.html', {'user_list': user_list, "page_html": html})

def edit_host(request,pk):
    if request.method == "GET":
        return render(request,'edit_host.html')
    else:
        url = "/hosts/?%s" %(request.GET.get('_list_filter'))
        return redirect(url)

def userinfo(request):
    u_list=models.Student.objects.all()
    pager_obj = Pagination(request.GET.get('page', 1), len(u_list), request.path_info, request.GET)
    u_list = u_list[pager_obj.start:pager_obj.end]

    html = pager_obj.page_html()

    return render(request, 'userinfo.html', {'u_list': u_list, "page_html": html})

class addModelForm(ModelForm):
    class Meta:
        model=models.Student
        fields="__all__"

def add(request):
    if request.method=="GET":
        form = addModelForm()
        return render(request,"add.html",{"form":form})
    else:
        form=addModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/userinfo/")


def ueduit(request,id):
    obj=models.Student.objects.filter(id=id).first()
    if request.method=="GET":
        form = addModelForm(instance=obj)
        return render(request,"edit.html",{"form":form})
    else:
        form=addModelForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/userinfo/")

def delete(request,nid):
    models.Student.objects.filter(pk=nid).delete()
    return redirect("/userinfo/")


