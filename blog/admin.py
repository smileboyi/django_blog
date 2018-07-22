from django.contrib import admin
from . import models
# Register your models here.

# Entry的管理器
class EntryAdmin(admin.ModelAdmin):
	list_display = ['title','author','visiting','created_time','modifyed_time']
	site_header = '博客管理系统'
	site_title = '博客'
	# 一般ManyToManyField多对多字段用过滤器；标题等文本字段用搜索框；日期时间用分层筛选。



# 在后台管理注册数据模型，后台进行管理注册的数据表
admin.site.register(models.Category)
admin.site.register(models.Tag)
# 模型和管理器关联，另一种写法@admin.register(Entry)
admin.site.register(models.Entry,EntryAdmin)
