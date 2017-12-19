
from django.conf.urls import url
from django.contrib import admin
from stark.service import v1
from app03 import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^stark/',v1.site.urls),
    url(r'^hosts/',views.hosts),
    url(r'^users/',views.users),
    url(r'^edit/',views.edit_host),
    url(r'^userinfo/',views.userinfo),
    url(r'^add/', views.add),
    url(r'^ueduit/(\d+)/', views.ueduit),
    url(r'^del/',views.delete),


]
