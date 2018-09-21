from django.conf.urls import url
from django.views.static import serve

from Supmakt.settings import MEDIA_ROOT
from login.views import *

urlpatterns = [
	url(r'^$', login_in_view, name='login_in_view'),
	url(r'^reg.html/$', registor_view, name='registor_view'),
	url(r'^infor.html/$', infor_view, name='infor_view'),
	url(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
]
