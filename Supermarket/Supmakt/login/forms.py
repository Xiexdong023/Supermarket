from django import forms
from django.forms import ModelForm

from login.models import UserTable


class UserForm(forms.Form):
	# name = forms.CharField(required=)
	pass

class UserModelForm(ModelForm):
	class Meta:
		model = UserTable
		fields = ['mobile', 'password']
		error_messages = {
			'mobile': {'required':'号码不能为空',
			           'max_length': '号码大于11位',
		                'min_length': '号码少于11位',
			           'unique':'用户已注册'},
			'password':{'required':'密码不能为空',
			            'max_length': '密码不能大于20位',
			            'min_length': '密码不能少于6位',
		                 },
		}

	# def clean_mobile(self):
	# 	self.cleaned_data.

