from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django import forms

from login.helper import hash_password
from login.models import UserTable


class UserModelForm(forms.ModelForm):
	repassword = forms.CharField(max_length=16,
	                             min_length=6,
	                             error_messages={'required': '请填写确认密码', },
	                             widget=forms.PasswordInput(attrs={'class': 'login-password',
	                                                               'placeholder': '请确认密码'}
	                                                        )
	                             )

	class Meta:
		model = UserTable
		fields = ['phone', 'password']
		error_messages = {
			'phone': {'required': '号码不能为空'},
			'password': {'required': '密码不能为空',
			             'max_length': '密码不能大于16个字符',
			             'min_length': '密码不能少于6个字符'},
		}
		widgets = {
			'phone': forms.TextInput(attrs={'class': 'login-name',
			                                'placeholder': '请输入手机号'}
			                         ),
			'password': forms.PasswordInput(attrs={'class': 'login-password',
			                                       'placeholder': '请输入密码'}
			                                ),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['password'].validators.append(validators.MaxLengthValidator(16))
		self.fields['password'].validators.append(validators.MinLengthValidator(6))

	def clean_phone(self):
		phone = self.cleaned_data.get('phone')
		user = UserTable.objects.filter(phone=phone).first()
		if user:
			raise forms.ValidationError('该账号已被注册')
		else:
			return phone

	def clean(self):
		cleaned_data = super().clean()
		pw1 = cleaned_data.get('password')
		pw2 = cleaned_data.get('repassword')
		if pw1 and pw2 and pw1 != pw2:
			raise forms.ValidationError({'repassword': '两次密码不一致'})
		else:
			if pw1:
				"""对密码进行加密处理"""
				cleaned_data['password'] = hash_password(pw1)
			return cleaned_data


class LoginForm(forms.ModelForm):
	class Meta:
		model = UserTable
		fields = ['phone', 'password']

		error_messages = {
			'phone': {'required': '电话输入为空'},
			'password': {'required': '密码输入为空'}
		}
		widgets = {
			'phone': forms.TextInput(attrs={'class': 'login-name',
			                                'placeholder': '请输入手机号'
			                                }
			                         ),
			'password': forms.PasswordInput(attrs={'class': 'login-password',
			                                       'placeholder': '请输入手机号'
			                                       }
			                                )
		}

	# def clean_phone(self):
	# 	phone = self.cleaned_data.get('phone')
	# 	user = UserTable.objects.filter(phone=phone).first()
	# 	if user is None:
	# 		raise forms.ValidationError("号码不存在,请注册")
	# 	else:
	# 		return phone

	def clean(self):
		cleaned_data = self.cleaned_data
		phone = cleaned_data.get('phone')
		user = UserTable.objects.filter(phone=phone).first()
		if user is None:
			raise forms.ValidationError({"phone": "号码不存在,请注册"})
		else:
			"""用户存在则判断密码是否正确"""
			password = cleaned_data.get('password')
			pwd_db = user.password
			password = hash_password(password)
			if pwd_db != password:
				raise forms.ValidationError({'password': '密码不正确'})
			else:
				cleaned_data['user'] = user
				return cleaned_data
