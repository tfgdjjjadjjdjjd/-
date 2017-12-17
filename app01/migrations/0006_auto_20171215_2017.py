# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-15 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_auto_20171215_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=32, verbose_name='主机名')),
                ('ip', models.GenericIPAddressField(verbose_name='IP')),
                ('post', models.IntegerField(verbose_name='端口名')),
            ],
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(max_length=32, verbose_name='用户邮箱'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='pwd',
            field=models.CharField(max_length=32, verbose_name='用户密码'),
        ),
    ]