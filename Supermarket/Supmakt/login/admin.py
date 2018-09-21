from django.contrib import admin

# Register your models here.
from login.models import *


@admin.register(InfoModel)
class InforAdmin(admin.ModelAdmin):
	pass


@admin.register(UserTable)
class UserAdmin(admin.ModelAdmin):
	pass
