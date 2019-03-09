"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from blog import views
from django.views.static import serve
from BBS import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # restful
    url(r'^users/$', views.Users.as_view()),
    url(r'^users2/$', views.user2),

    url(r'^$', views.home),
    # 注册
    url(r'^register/$', views.register),
    # 登入
    url(r'^login/$', views.login),
    # 随机验证码
    url(r'^get_valid_code/$', views.get_valid_code),
    # 博客主页
    url(r'^index/$', views.index),
    # 退出
    url(r'^login_out/$', views.login_out),
    # 修改密码
    url(r'^change_password/$', views.change_password),
    # error错误信息
    url(r'^error/$', views.error),
    # 修改头像
    url(r'^change_avatar/$', views.change_avatar),
    # 点赞点踩
    url(r'^diggit/$', views.diggit),
    # 点评
    url(r'^comment/$', views.comment),
    # 后台管理
    url(r'^backend/$', views.backend),
    # 后台添加文章
    url(r'^add_article/$', views.add_article),
    # 文章修改
    url(r'^modification_article/$', views.modification_article),
    # 删除文章
    url(r'^delete_article/$', views.delete_article),
    # 添加文章上传图片add_img
    url(r'^add_img/$', views.add_img),

    # 个人站点的文章详情路由
    url(r'^(?P<username>\w+)/article/(?P<article_id>\d+)', views.article_detail),
    # 个人站点的分类路由
    url(r'^(?P<username>\w+)/(?P<condition>category|tag|archive)/(?P<param>.*)', views.blog_site),
    # media文件夹配置,用户可以无限制访问
    url(r'^media(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    # 个人站点
    url(r'^(?P<username>\w+)', views.blog_site),
]
