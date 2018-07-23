from django import template
from ..models import Entry,Category,Tag

# register的名字是固定的,不可改变
register = template.Library()

'''
https://www.cnblogs.com/liluning/p/7724699.html
如果是自定义过滤器加@register.filter装饰器
如果是自定义标签加@register.simple_tag装饰器(类似于vuex getters)
过滤器函数的参数只能有两个，自定义标签无参数限制
过滤器可以与逻辑标签共同使用，比如if标签。自定义标签不可以。
'''

@register.simple_tag
def get_recent_entries(num=5):
	return Entry.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def get_popular_entries(num=5):
	return Entry.objects.all().order_by('-visiting')[:num]


@register.simple_tag
def get_categories():
	return Category.objects.all()


# 分类文章数量
@register.simple_tag
def get_entry_count_of_category(category_name):
	return Entry.objects.filter(category__name=category_name).count()


@register.simple_tag
def archives():
	return Entry.objects.dates('created_time','month',order='DESC')


@register.simple_tag
def get_entry_count_of_date(year,month):
	return Entry.objects.filter(created_time__year=year,created_time__month=month).count()