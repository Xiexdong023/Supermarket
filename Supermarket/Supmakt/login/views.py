from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

# Create your views here.
from django.views import View

from login.forms import *
from login.models import *


class LoginView(View):
	"""登录账户"""

	def get(self, request):
		form = LoginForm()
		context = {
			'form': form
		}
		return render(request, 'login/login.html', context)

	def post(self, request):
		form = LoginForm(request.POST)
		if form.is_valid():
			"""验证成功"""
			# 注册session
			user = form.cleaned_data.get('user')
			request.session['ID'] = user.pk
			request.session['phone'] = user.phone
			request.session.set_expiry(0)
			return redirect(reverse('login:center_View'))
		else:
			context = {
				'form': form
			}
			return render(request, 'login/login.html', context)


# user = UserTable.objects.filter(phone=phone)


class RegistorView(View):
	"""注册账户"""

	def get(self, request):
		form = UserModelForm()
		context = {
			'form': form
		}
		return render(request, 'login/reg.html', context)

	def post(self, request):
		# 1.接收数据
		# 2.验证数据
		form = UserModelForm(request.POST)
		if form.is_valid():
			"""验证通过"""
			form.save()
			return redirect(reverse("login:login_in_view"))
		else:
			"""验证失败"""
			context = {
				'form': form
			}
		return render(request, 'login/reg.html', context)


class InforView(View):
	def get(self, request):
		return render(request, 'login/infor.html')

	def post(self, request):
		pass


class CenterView(View):
	def get(self, request):
		return render(request, 'index/member.html')

	def post(self, request):
		pass
