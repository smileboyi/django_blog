from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
	path(r'^$',views.index,name='blog_index'),
	path(r'^(?P<blog_id>[0-9]+)',views.detail,name='blog_detail'),
]