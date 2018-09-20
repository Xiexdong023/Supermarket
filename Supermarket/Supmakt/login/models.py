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
	name = models.CharField(max_length=10, verbose_name='昵称')
	password = models.CharField(max_length=20,
	                            validators=[validators.MinLengthValidator(6)],
	                            verbose_name='密码',
	                            )
	sex_choices = (
		(1, '男'),
		(2, '女'),
		(3, '保密'),
	)
	sex = models.SmallIntegerField(choices=sex_choices, default=1)
	school = models.CharField(max_length=100, null=True)
	home = models.CharField(max_length=100, null=True)
	add_date = models.DateField(auto_now_add=True)  # auto_now_add:第一次添加,使用当前时间
	modify_date = models.DateField(auto_now_add=True)  # add_date:每次修改使用当前时间
	delete_flag = models.BooleanField(default=False)

	class Meta:
		db_table = 'users'
