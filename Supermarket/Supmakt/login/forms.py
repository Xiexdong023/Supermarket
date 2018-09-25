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

	verify = forms.CharField(required=True,
	                         widget=forms.TextInput(attrs={'class': 'reg-yzm',
	                                                       'placeholder': '输入验证码'}
	                                                ),
	                         error_messages={'required': '验证码为空'}
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

	def clean_verify(self):
		verify_code = self.data.get('verify')
		session_code = self.data.get('session_code')
		if session_code is None:
			raise forms.ValidationError('请先获取验证码')
		if verify_code != session_code:
			raise forms.ValidationError('验证码错误')
		return

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
			                                       'placeholder': '请输入密码'
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
			password = cleaned_data.get('password', '')
			pwd_db = user.password
			password = hash_password(password)
			if pwd_db != password:
				raise forms.ValidationError({'password': '密码不正确'})
			else:
				cleaned_data['user'] = user
				return cleaned_data


class InforForm(forms.ModelForm):
	sex_choices = (
		(1, '男'),
		(2, "女"),
		(3, "保密"),
	)

	class Meta:
		model = UserTable
		fields = ['nickname', 'birthday', 'head', 'gender',
		          'school_name', 'address', 'hometown', 'phone']
		widgets = {
			'nickname': forms.TextInput(attrs={'class': 'infor-tele', 'placeholder': '默契'}),
			'birthday': forms.TextInput(attrs={'class': 'infor-tele', 'placeholder': '1991-10-15'}),
			'school_name': forms.TextInput(attrs={'class': 'infor-tele', 'placeholder': '就读于哪个学校'}),
			'address': forms.TextInput(attrs={'class': 'infor-tele', 'placeholder': '详细地址'}),
			'hometown': forms.TextInput(attrs={'class': 'infor-tele', 'placeholder': '来自哪里'}),
			'phone': forms.TextInput(attrs={'class': 'infor-tele', 'placeholder': '13012345678'}),

			# 'gender': {'class': 'infor-tele', 'placeholder': 'adfa'},
			# 'head': {'class': 'daf', 'placeholder': 'adfa'},
			# 'birthday': {'class': 'infor-tele', 'placeholder': '1991-11-05'},
			# 'school_name': {'class': 'infor-tele', 'placeholder': '就读于哪个学校'},
			# 'address': {'class': 'infor-tele', 'placeholder': '详细地址'},
			# 'hometown': {'class': 'infor-tele', 'placeholder': '来自哪里'},
			# 'phone': {'class': 'infor-tele', 'placeholder': '13012345678'},
		}

# def clean(self):
# 	cleaned_data = super().clean()
# 	return cleaned_data
