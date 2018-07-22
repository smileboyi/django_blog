from django import template
from ..models import Entry,Category,Tag

# register的名字是固定的,不可改变
register = template.Library()

'''
https://www.cnblogs.com/liluning/p/7724699.html
如果是自定义过滤器加@register.filter装饰器
如果是自定义标签加@register.simple_tag装饰器
过滤器函数的参数只能有两个，自定义标签无参数限制
过滤器可以与逻辑标签共同使用，比如if标签。自定义标签不可以。
'''

@register.simple_tag
def get_recent_entries(num=5):
	return Entry.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def get_popular_entries(num=5):
	return Entry.objects.all().order_by('-visiting')[:num]

