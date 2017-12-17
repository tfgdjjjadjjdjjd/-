from django.shortcuts import HttpResponse
from django.utils.safestring import mark_safe
from stark.service import v1
from app01 import models

class UserInfoConfig(v1.StarkConfig):


    list_display = ['id','name','email','pwd','ut']

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
