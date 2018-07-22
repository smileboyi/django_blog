# from django.urls import path
from django.conf.urls import url,include
from . import views

app_name = 'blog'

urlpatterns = [
	# path(r'^$',views.index,name='blog_index'),
	url(r'^$', views.index,name='blog_index'),
	url(r'^(?P<blog_id>[0-9]+)',views.detail,name='blog_detail'),
]