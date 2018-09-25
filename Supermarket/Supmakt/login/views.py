from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse

# Create your views here.
from django.views import View

from login.forms import *
from login.models import *


class LoginView(View):
	"""登录账户"""

	def get(self, request):
		id = request.session.get('ID')
		if not id:
			# 若账号不存在
			form = LoginForm()
			context = {
				'form': form
			}
			return render(request, 'login/login.html', context)
		user = UserTable.objects.filter(pk=id).first()
		context = {
			"user": user
		}
		return render(request, 'goods/member.html', context)

	def post(self, request):
		form = LoginForm(request.POST)
		if form.is_valid():
			"""验证成功"""
			# 注册session
			user = form.cleaned_data.get('user')
			request.session['ID'] = user.pk
			request.session['phone'] = user.phone
			request.session.set_expiry(0)

			return redirect(reverse('login:login_in_view'))
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
		data = request.POST.dict()
		session_code = request.session.get('session_code')
		data['session_code'] = session_code

		form = UserModelForm(data)
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
		id = request.session.get('ID')
		user = UserTable.objects.filter(pk=id).first()
		show_info = user.head
		form = InforForm(instance=user)
		context = {
			'form': form,
			'user': user
		}
		return render(request, 'login/infor.html', context)

	def post(self, request):
		id = request.session.get('ID')
		user = UserTable.objects.filter(pk=id).first()
		"""修改数据"""
		form = InforForm(request.POST, request.FILES, instance=user)
		form.save()
		# user.head = request.FILES['head']
		# user.nickname = request.POST.get('nickname')
		# user.gender = request.POST.get('gender')
		# user.birthday = request.POST.get('birthday')
		# user.school_name = request.POST.get('school_name')
		# user.address = request.POST.get('address')
		# user.hometown = request.POST.get('hometown')
		# user.phone = request.POST.get('phone')
		# form = InforForm(request.POST)
		# user.save()
		return redirect(reverse('login:center_View'))


# else:
# 	return render(request, 'login/infor.html')


class CenterView(View):
	def get(self, request):
		id = request.session.get('ID')
		if not id:
			user = UserTable.objects.filter(pk=id).first()
			context = {
				'user': user
			}
			return render(request, 'goods/member.html', context)
		return redirect(reverse('login:login_in_view'))


class SendCodeView(View):
	"""生成验证码"""

	def post(self, request):
		mobile = request.POST.get('mobile')  # 获取html表单提交过来的电话号码
		res = UserTable.objects.filter(phone=mobile).exists()
		if res:
			"""若填写的电话号码已存在 则提示用户已存在"""
			data = {'status': '403', 'message': '该用户已注册,请直接登录'}
		else:
			"""进行验证"""
			import random
			codelist = [str(random.randint(0, 9)) for _ in range(0, 4)]
			num_code = ''.join(codelist)  # 模拟生成随机验证码
			request.session['session_code'] = num_code  # 保存系统生成的验证码
			request.session.set_expiry(60)
			print('**********{}***************'.format(num_code))
			data = {'status': '200',
			        'session_code': num_code}
		return JsonResponse(data)


class QuitView(View):
	def get(self, request):
		request.session.clear()
		return redirect(reverse('index:index_view'))

	def post(self, request):
		pass
