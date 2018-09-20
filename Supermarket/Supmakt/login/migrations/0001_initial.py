# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-20 09:02
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(error_messages={'max_length': '号码大于11位', 'min_length': '号码少于11位'}, max_length=11, validators=[django.core.validators.MinLengthValidator(11), django.core.validators.RegexValidator('^1[3-9]\\d{9}', '号码格式错误')], verbose_name='用户手机号')),
                ('name', models.CharField(max_length=10, verbose_name='昵称')),
                ('password', models.CharField(error_messages={'max_length': '密码不大于20位', 'min_length': '密码不少于6位'}, max_length=20, validators=[django.core.validators.MinLengthValidator(6)], verbose_name='密码')),
                ('sex', models.SmallIntegerField(choices=[(1, '男'), (2, '女'), (3, '保密')], default=1)),
                ('school', models.CharField(max_length=100, null=True)),
                ('home', models.CharField(max_length=100, null=True)),
                ('add_date', models.DateField(auto_now_add=True)),
                ('modify_date', models.DateField(auto_now_add=True)),
                ('delete_flag', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
