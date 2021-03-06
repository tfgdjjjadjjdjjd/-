# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-15 09:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_usertype'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(default=2, max_length=32, verbose_name='邮箱'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='pwd',
            field=models.CharField(default=2, max_length=32, verbose_name='密码'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='ut',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app01.UserType', verbose_name='用户类型'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='name',
            field=models.CharField(max_length=32, verbose_name='用户名称'),
        ),
        migrations.AlterField(
            model_name='usertype',
            name='name',
            field=models.CharField(max_length=32, verbose_name='类型名称'),
        ),
    ]
