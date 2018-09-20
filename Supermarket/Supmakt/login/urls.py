from django.conf.urls import url

from login.views import *

urlpatterns = [
	url(r'^$', login_in_view, name='login_in_view'),
	url(r'^reg.html/$', registor_view, name='registor_view'),
]