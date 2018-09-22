from datetime import datetime

from django.core import validators
from django.db import models


# Create your models here.
class UserTable(models.Model):
	mobile = models.CharField(validators=[validators.MinLengthValidator(11),
	                                      validators.RegexValidator(r'^\d+', '号码必须为数字')],
	                          max_length=11,
	                          verbose_name='用户手机号',
	                          unique=True,
	                          )

	password = models.CharField(max_length=20,
	                            validators=[validators.MinLengthValidator(6)],
	                            verbose_name='密码',
	                            )
	# name = models.CharField(max_length=10, verbose_name='昵称')
	# sex_choices = (
	# 	(1, '男'),
	# 	(2, '女'),
	# 	(3, '保密'),
	# )
	# sex = models.SmallIntegerField(choices=sex_choices, default=1)
	# school = models.CharField(max_length=100, null=True)
	# home = models.CharField(max_length=100, null=True)
	add_date = models.DateField(auto_now_add=True)  # auto_now_add:第一次添加,使用当前时间
	modify_date = models.DateField(auto_now_add=True)  # add_date:每次修改使用当前时间
	delete_flag = models.BooleanField(default=False)

	class Meta:
		db_table = 'users'
		verbose_name = "用户注册表"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.mobile


class InfoModel(models.Model):
	img = models.ImageField(upload_to='img', default='images/infortx.png',
	                        verbose_name='人员头像')
	name = models.CharField(max_length=20,
	                        verbose_name='昵称')
	sex_choices = (
		(1, '男'),
		(2, '女'),
	)
	sex = models.SmallIntegerField(choices=sex_choices, default=1,
	                               verbose_name='性别')
	birthday = models.CharField(max_length=20, verbose_name='生日')
	school = models.CharField(max_length=100, verbose_name='学校')
	address = models.CharField(max_length=100, verbose_name='地址')
	home = models.CharField(max_length=100, verbose_name='家乡')
	phonenum = models.CharField(max_length=11, verbose_name='手机号')
	# 设置一对一的关联关系,设置修改模式为级联
	infor = models.OneToOneField(to='UserTable', primary_key=True, default=1)

	class Meta:
		db_table = 'information'
		verbose_name = "用户基本信息表"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name
