from django.conf.urls import url
from django.shortcuts import HttpResponse,render,redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.http import QueryDict
from django.db.models import Q


class ChangeList(object):
    def __init__(self,config,queryset):
        self.config = config

        # [checkbox,'id','name',edit,del]
        self.list_display = config.get_list_display()
        self.model_class = config.model_class
        self.request = config.request
        self.show_add_btn = config.get_show_add_btn()
        self.actions = config.get_actions()
        self.show_actions = config.get_show_actions()

        # 搜索用运
        self.show_search_form = config.get_show_search_form()
        self.search_form_val = config.request.GET.get(config.search_key,'')

        # 分页处理

        from components.pager import Pagination
        current_page = self.request.GET.get('page', 1)
        total_count = queryset.count()
        page_obj = Pagination(current_page, total_count, self.request.path_info, self.request.GET, per_page_count=8)
        self.page_obj = page_obj

        self.data_list = queryset[page_obj.start:page_obj.end]

    def modify_actions(self):
        result = []
        for func in self.actions:
            temp = {'name':func.__name__,'text':func.short_desc}
            result.append(temp)
        return result

    def add_url(self):
        return self.config.get_add_url()

    def head_list(self):
        """
        构造表头
        :return:
        """
        result = []
        # [checkbox,'id','name',edit,del]
        for field_name in self.list_display:
            if isinstance(field_name, str):
                # 根据类和字段名称，获取字段对象的verbose_name
                verbose_name = self.model_class._meta.get_field(field_name).verbose_name
            else:
                verbose_name = field_name(self.config, is_header=True)
            result.append(verbose_name)
        return result

    def body_list(self):
        # 处理表中的数据
        # [ UserInfoObj,UserInfoObj,UserInfoObj,UserInfoObj,]
        # [ UserInfo(id=1,name='alex',age=18),UserInfo(id=2,name='alex2',age=181),]
        data_list = self.data_list
        new_data_list = []
        for row in data_list:
            # row是 UserInfo(id=2,name='alex2',age=181)
            # row.id,row.name,row.age
            temp = []
            for field_name in self.list_display:
                if isinstance(field_name,str):
                    val = getattr(row,field_name) # # 2 alex2
                else:
                    val = field_name(self.config,row)
                temp.append(val)
            new_data_list.append(temp)

        return new_data_list

class StarkConfig(object):

    # 1. 定制列表页面显示的列
    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return '选择'
        return mark_safe('<input type="checkbox" name="pk" value="%s" />' %(obj.id,))
    def edit(self,obj=None,is_header=False):
        if is_header:
            return '编辑'
        # 获取条件
        query_str = self.request.GET.urlencode() # page=2&nid=1
        if query_str:
            # 重新构造
            params = QueryDict(mutable=True)
            params[self._query_param_key] = query_str
            return mark_safe('<a href="%s?%s">编辑</a>' %(self.get_change_url(obj.id),params.urlencode(),)) # /stark/app01/userinfo/
        return mark_safe('<a href="%s">编辑</a>' % (self.get_change_url(obj.id),))  # /stark/app01/userinfo/

    def delete(self,obj=None,is_header=False):
        if is_header:
            return '删除'
        return mark_safe('<a href="%s">删除</a>' %(self.get_delete_url(obj.id),))

    list_display = []

    def get_list_display(self):
        data = []
        if self.list_display:
            data.extend(self.list_display)
            data.append(StarkConfig.edit)
            data.append(StarkConfig.delete)
            data.insert(0,StarkConfig.checkbox)
        return data

    # 2. 是否显示添加按钮
    show_add_btn = True

    def get_show_add_btn(self):
        return self.show_add_btn

    # 3. model_form_class
    model_form_class = None
    def get_model_form_class(self):
        if self.model_form_class:
            return self.model_form_class

        from django.forms import ModelForm
        # class TestModelForm(ModelForm):
        #     class Meta:
        #         model = self.model_class
        #         fields = "__all__"
        # 作业：type创建TestModelForm类
        meta = type('Meta',(object,),{'model':self.model_class,'fields':'__all__'})
        TestModelForm = type('TestModelForm',(ModelForm,),{'Meta':meta})
        return TestModelForm

    # 4. 关键字搜索
    show_search_form = False
    def get_show_search_form(self):
        return self.show_search_form

    search_fields = []
    def get_search_fields(self):
        result = []
        if self.search_fields:
            result.extend(self.search_fields)

        return result

    def get_search_condition(self):
        key_word = self.request.GET.get(self.search_key)
        search_fields = self.get_search_fields()
        condition = Q()
        condition.connector = 'or'
        if key_word and self.get_show_search_form():
            for field_name in search_fields:
                condition.children.append((field_name, key_word))
        return condition

    # 5. actions定制
    show_actions = False
    def get_show_actions(self):
        return self.show_actions

    actions = []
    def get_actions(self):
        result = []
        if self.actions:
            result.extend(self.actions)
        return result


    def __init__(self,model_class,site):
        self.model_class = model_class
        self.site = site

        self.request = None
        self._query_param_key = "_listfilter"
        self.search_key = "_q"

    # ############# URL 相关 ###############
    def wrap(self,view_func):
        def inner(request,*args,**kwargs):
            self.request = request
            return view_func(request,*args,**kwargs)
        return inner
    def get_urls(self):
        app_model_name = (self.model_class._meta.app_label,self.model_class._meta.model_name,)
        url_patterns = [
            url(r'^$',self.wrap(self.changelist_view),name="%s_%s_changlist" %app_model_name),
            url(r'^add/$',self.wrap(self.add_view),name="%s_%s_add" %app_model_name),
            url(r'^(\d+)/delete/$',self.wrap(self.delete_view),name="%s_%s_delete" %app_model_name),
            url(r'^(\d+)/change/$',self.wrap(self.change_view),name="%s_%s_change" %app_model_name),
        ]
        url_patterns.extend(self.extra_url())
        return url_patterns
    def extra_url(self):
        return []
    @property
    def urls(self):
        return self.get_urls()
    def get_change_url(self,nid):
        name = "stark:%s_%s_change" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        edit_url = reverse(name, args=(nid,))
        return edit_url
    def get_list_url(self):
        name = "stark:%s_%s_changlist" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        edit_url = reverse(name)
        return edit_url
    def get_add_url(self):
        name = "stark:%s_%s_add" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        edit_url = reverse(name)
        return edit_url
    def get_delete_url(self,nid):
        name = "stark:%s_%s_delete" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        edit_url = reverse(name,args=(nid,))
        return edit_url
    # ############# 处理请求的方法 ################

    def changelist_view(self,request,*args,**kwargs):
        """
        /stark/app01/userinfo/    self.model_class=models.UserInfo
		/stark/app01/role/        self.model_class=models.Role
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        if request.method == 'POST' and self.get_show_actions():
            func_name_str = request.POST.get('list_action')
            action_func = getattr(self,func_name_str)
            ret = action_func(request)
            if ret:
                return ret

        queryset = self.model_class.objects.filter(self.get_search_condition())
        cl = ChangeList(self,queryset)
        return render(request,'stark/changelist.html',{'cl':cl})

    def add_view(self,request,*args,**kwargs):

        model_form_class = self.get_model_form_class()
        if request.method == "GET":
            form = model_form_class()
            return render(request,'stark/add_view.html',{'form':form})
        else:
            form = model_form_class(request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.get_list_url())
            return render(request, 'stark/add_view.html', {'form': form})

    def change_view(self,request,nid,*args,**kwargs):
        # self.model_class.objects.filter(id=nid)
        obj = self.model_class.objects.filter(pk=nid).first()
        if not obj:
            return redirect(self.get_list_url())

        model_form_class = self.get_model_form_class()
        # GET,显示标签+默认值
        if request.method == 'GET':
            form = model_form_class(instance=obj)
            return render(request,'stark/change_view.html',{'form':form})
        else:
            form = model_form_class(instance=obj,data=request.POST)
            if form.is_valid():
                form.save()
                list_query_str = request.GET.get(self._query_param_key)
                list_url = "%s?%s" %(self.get_list_url(),list_query_str,)
                return redirect(list_url)
            return render(request, 'stark/change_view.html', {'form': form})



        return HttpResponse('修改')

    def delete_view(self,request,nid,*args,**kwargs):
        self.model_class.objects.filter(pk=nid).delete()
        return redirect(self.get_list_url())


class StarkSite(object):
    def __init__(self):
        self._registry = {}

    def register(self,model_class,stark_config_class=None):
        if not stark_config_class:
            stark_config_class = StarkConfig
        self._registry[model_class] = stark_config_class(model_class,self)

    def get_urls(self):
        url_pattern = []

        for model_class,stark_config_obj in self._registry.items():
            # 为每一个类，创建4个URL
            """
            {
                models.UserInfo: StarkConfig(models.UserInfo,self),
                models.Role: StarkConfig(models.Role,self)
            }
            /stark/app01/userinfo/
            /stark/app01/userinfo/add/
            /stark/app01/userinfo/(\d+)/change/
            /stark/app01/userinfo/(\d+)/delete/
            """
            app_name = model_class._meta.app_label
            model_name = model_class._meta.model_name

            curd_url = url(r'^%s/%s/' %(app_name,model_name,) , (stark_config_obj.urls,None,None))
            url_pattern.append(curd_url)


        return url_pattern

    @property
    def urls(self):
        return (self.get_urls(),None,'stark')

site = StarkSite()