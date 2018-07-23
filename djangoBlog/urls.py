"""djangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# 路由系统：旧django.conf.urls，新django.urls
from django.conf.urls import url,include

from django.conf import settings
from django.conf.urls.static import static

from blog.feed import LatestEntriesFeed

from blog import views as blog_views

from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from blog.models import Entry

info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'modifyed_time'
}

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^blog/',include('blog.urls')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^latest/feed/$', LatestEntriesFeed()),    #RSS订阅
    # 如果sitemap.xml位于根目录中，它会引用网站中的任何URL。 但是如果站点地图位于/content/sitemap.xml，则它只能引用以/content/开头的网址。
    # 使用GenericSitemap构造一个GenericSitemap类型的数据，priority为更新频率0-1之间
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'blog': GenericSitemap(info_dict, priority=0.6)}},
      name='django.contrib.sitemaps.views.sitemap'),       #站点地图
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT ) #添加图片的url


# 需要DEBUG = False
handler403 = blog_views.permission_denied
handler404 = blog_views.page_not_found
handler500 = blog_views.page_error
