from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

# Create your views here.
from login.forms import *
from login.models import *


def login_in_view(request):
	"""登录账户"""
	# return HttpResponse("ok")
	# UserTable
	if request.method == "POST":
		data = request.POST
		try:
			# 根据输入的用户名和密码验证登录,成功则返回一个用户对象
			user = UserTable.objects.get(mobile=data['mobile'], password=data['password'])
			"""登录成功后执行的操作"""
			request.session['userID'] = user.pk  # 获取用户登录账号到session中
			request.session.set_expiry(0)  # 设置过期时间为退出浏览器过期
			# print('successfully')
			url = reverse('login:infor_view')
			return redirect(url)
		except Exception:
			context = {
				'reload': '请重新登录'
			}
			return render(request, "login/login.html", context)
	else:
		return render(request, "login/login.html")


def registor_view(request):
	"""注册账户"""
	if request.method == 'POST':
		data = request.POST
		try:
			if data['checkbox'] == '同意':
				"""判断用户协议是否勾选"""
				pass
			# 生成form对象
			form = UserModelForm(data)
			# 验证
			if form.is_valid():
				# 数据保存到数据库
				form.save()
				return render(request, 'login/login.html')
			else:
				context = {
					"form": form,
					"passwordError": form.errors['__all__'][0],
				}
				return render(request, 'login/reg.html', context)
		except Exception:
			"""用户协议未勾选则提示"""
			context = {
				"agreed": "请同意协议"
			}
			return render(request, 'login/reg.html', context)
	else:
		return render(request, 'login/reg.html')


def infor_view(request):
	try:
		userID = request.session.get('userID', '0')  # 获取session上当前登录用户ID信息
		userID = int(userID)
		if userID:
			"""获取的userID为用户ID"""
			user = UserTable.objects.get(pk=userID)  # 获取UserTable模型对象
			if request.method == "POST":
				"""POST方式提交用户修改后的数据"""
				# data = request.POST
				# InfoModel.objects.create(infor=user,
				#                          name=data.name,
				#                          sex=data.sex,
				#                          birthday=data.birthday,
				#                          school=data.school,
				#                          address=data.address,
				#                          home=data.home,
				#                          phonenum=data.phonenum)
				return render(request, 'login/infor.html')
			else:
				"""
				GET方式访问用户基本信息页面
				1.需要数据回显
				2.需要获取当前登录用户的ID userID = request.session.get['userID']
				"""

				# """**************此处做异常处理,后期添加"""
				try:
					"""若information表中有数据,则查询,若没有则直接跳入infor编辑页面"""
					infor_obj = user.infomodel  # 获取基本信息模型对象
					form = UserModelForm(instance=infor_obj)  # 模型表单验证模型对象,回显数据
					show_info = form.instance
					context = {
						"show_info": show_info
					}
					return render(request, 'login/infor.html', context)
				except Exception:
					return render(request, 'login/infor.html')
		else:
			print("获取session的userID为0")
	except Exception:
		print("获取session出错")
