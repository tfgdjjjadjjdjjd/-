# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-15 09:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_auto_20171215_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(default=1, max_length=32, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='pwd',
            field=models.CharField(default=1, max_length=32, verbose_name='密码'),
        ),
    ]
