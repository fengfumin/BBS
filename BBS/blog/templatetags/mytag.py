# -*- coding: utf-8 -*-
"""
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

from django.template import Library
from blog import models
# 时间分组组件
from django.db.models.functions import TruncMonth
from django.db.models import Count

register = Library()


@register.inclusion_tag("category_tag.html")
def category_tag(username):
    user = models.UserInfo.objects.filter(username=username).first()

    blog = user.blog
    # 查询出标签分类的名字和数量
    tag_res = models.Tag.objects.filter(blog=blog).values("pk").annotate(c=Count("article")).values_list('name', "c",
                                                                                                         'pk').order_by("pk")
    # 查询出随笔分类的名字和数量
    category_res = models.Category.objects.filter(blog=blog).values("pk").annotate(c=Count("article")).values_list(
        'name', "c", 'pk')
    # 查询出时间分类的名字和数量
    month_res = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth("var_time")).values(
        "month").annotate(c=Count("pk")).values_list("month", "c")

    return {"tag_res": tag_res, "category_res": category_res, "month_res": month_res, "user": user}
