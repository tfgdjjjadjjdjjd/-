from django.shortcuts import HttpResponse,redirect
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from stark.service import v1
from app01 import models


class UserInfoModelForm(ModelForm):
    class Meta:
        model = models.UserInfo
        fields = '__all__'
        error_messages = {
            'name':{
                'required':'用户名不能为空'
            }
        }


class UserInfoConfig(v1.StarkConfig):


    list_display = ['id','name','email','pwd','ut']

    show_add_btn = True

    model_form_class = UserInfoModelForm

    show_search_form = True

    search_fields = ['name__contains', 'email__contains']

    show_actions = True

    def multi_del(self, request):
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()
        # return HttpResponse('删除成功')
        return redirect("http://www.baidu.com")

    multi_del.short_desc = "批量删除"

    def multi_init(self, request):
        pk_list = request.POST.getlist('pk')
        # self.model_class.objects.filter(id__in=pk_list).delete()
        # return HttpResponse('删除成功')
        # return redirect("http://www.baidu.com")

    multi_init.short_desc = "初始化"

    actions = [multi_del, multi_init]


v1.site.register(models.UserInfo,UserInfoConfig) # UserInfoConfig(UserInfo,)


class RoleConfig(v1.StarkConfig):
    list_display = ['name',]
v1.site.register(models.Role,RoleConfig) # StarkConfig(Role)

class UserTypeConfig(v1.StarkConfig):
    list_display = ['id','name']
v1.site.register(models.UserType,UserTypeConfig) # StarkConfig(Role)

class HostConfig(v1.StarkConfig):
    list_display = ['id','hostname','ip','post']

v1.site.register(models.Host,HostConfig)
