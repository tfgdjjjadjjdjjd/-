from django.db import models
class Role(models.Model):
    name=models.CharField(max_length=32)

    def __str__(self):
        return self.name


class UserType(models.Model):
    name=models.CharField(max_length=32,verbose_name='类型名称')

    def __str__(self):
        return self.name

class UserInfo(models.Model):
    name = models.CharField(max_length=32,verbose_name='用户名称')
    email = models.EmailField(verbose_name='用户邮箱', max_length=32)
    pwd = models.CharField(verbose_name='用户密码', max_length=32)
    ut = models.ForeignKey(verbose_name='用户类型', to="UserType", default=1)
    def __str__(self):
        return self.name


class Host(models.Model):
    hostname=models.CharField(max_length=32,verbose_name='主机名')
    ip=models.GenericIPAddressField(verbose_name='IP',protocol="both")
    post=models.IntegerField(verbose_name='端口名')
