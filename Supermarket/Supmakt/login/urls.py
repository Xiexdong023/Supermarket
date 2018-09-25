from django.conf.urls import url
from django.views.static import serve
from login.views import *

urlpatterns = [
	url(r'^$', LoginView.as_view(), name='login_in_view'),
	url(r'^reg.html/$', RegistorView.as_view(), name='registor_view'),
	url(r'^infor.html/$', InforView.as_view(), name='infor_view'),
	url(r'^center/$', CenterView.as_view(), name='center_View'),
	url(r'^SendCode/$', SendCodeView.as_view(), name='SendCodeView'),
	url(r'^quit/$', QuitView.as_view(), name='QuitView'),
]
