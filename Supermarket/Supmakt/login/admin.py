from django.contrib import admin

# Register your models here.
from login.models import *


@admin.register(UserTable)
class UserAdmin(admin.ModelAdmin):
	list_per_page = 10  # 每页显示条数
	actions_on_top = True  # 操作是否在上面显示, 默认True
	# actions_on_bottom = True  # 操作是否在下面显示, 默认False
	# list_display = [模型字段1, 模型字段2, ...]
	# list_display_links = []设置在列表页字段上添加一个a标签, 从而进入到编辑页面
	# list_filter = []: 列表右侧栏过滤器
	# search_fields=[] :搜索框,用于对指定字段的值进行搜索，支持模糊查询。列表类型，表示在这些字段上进行搜索。
