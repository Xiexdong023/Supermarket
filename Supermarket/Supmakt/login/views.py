from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from login.forms import UserModelForm
from login.models import UserTable

"""登录账户"""
def login_in_view(request):
	# return HttpResponse("ok")
	# UserTable
	if request.method == "POST":
		data = request.POST
		try:
			stu = UserTable.objects.get(mobile=data['mobile'], password=data['password'])
			print('successfully')
		except Exception:
			print("fail")

		print(data['mobile'])
		print(data['password'])
		return render(request, "login/login.html")
	else:
		return render(request, "login/login.html")


"""注册账户"""
def registor_view(request):
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
					"form": form
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
