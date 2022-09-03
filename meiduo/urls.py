"""meiduo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls

urlpatterns = [
                  path('admin/', admin.site.urls),
                  # 验证码模块
                  path('verifications/api/v1/', include("meiduo.apps.verifications.urls")),
                  # 用户模块
                  path('user/api/v1/', include("meiduo.apps.users.urls")),
                  # 第三方登陆
                  path('oauth/', include('meiduo.apps.oauth.urls')),
                  # 配置接口文档
                  path('docs/', include_docs_urls(title="美客网接口文档")),
                  # 行政区域
                  path("areas/api/v1/", include("meiduo.apps.areas.urls")),

                  # 富⽂本编辑器
                  re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),

                  # 定时任务
                  path("scheduler/", include('meiduo.apps.apschedulers.urls')),
                  # 商品
                  path("goods/api/v1/", include('meiduo.apps.goods.urls')),
                  # 购物车
                  path("carts/api/v1/", include('meiduo.apps.carts.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
