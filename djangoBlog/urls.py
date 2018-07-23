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


urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^blog/',include('blog.urls')),
    url(r'^latest/feed/$', LatestEntriesFeed()),    #RSS订阅
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT ) #添加图片的url
