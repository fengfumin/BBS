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

from django import forms
from django.forms import widgets
from blog import models
from django.core.exceptions import ValidationError


# forms组件类
class RegForm(forms.Form):
    # 各名字要与userinfo表字段名字一致
    username = forms.CharField(min_length=3, max_length=8, label='用户名',
                               error_messages={"min_length": "用户名太短了", "max_length": "用户名太长了",
                                               "required": "用户名不能为空"},
                               widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入用户名"}))
    password = forms.CharField(min_length=3, max_length=8, label='密码',
                               error_messages={"min_length": "密码太短了", "max_length": "密码太长了",
                                               "required": "密码不能为空"},
                               widget=widgets.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入密码"}))
    re_password = forms.CharField(min_length=3, max_length=8, label='确认密码',
                                  error_messages={"min_length": "确认密码太短了", "max_length": "确认密码太长了",
                                                  "required": "确认密码不能为空"},
                                  widget=widgets.PasswordInput(
                                      attrs={"class": "form-control", "placeholder": "请输入确认密码"}))
    email = forms.EmailField(label='邮箱',
                             error_messages={'invalid': '邮箱格式不合法',
                                             "required": "邮箱不能为空"},
                             widget=widgets.EmailInput(attrs={"class": "form-control", "placeholder": "请输入邮箱"}))
    mobile_phone = forms.IntegerField(min_value=10000000000, max_value=99999999999, label='手机号', required=False,
                                   error_messages={"min_value": "手机号必须是11位数", "max_value": "手机号必须是11位数",
                                                   },
                                   widget=widgets.NumberInput(
                                       attrs={"class": "form-control", "placeholder": "请输入手机号,可以不填", }))

    # 局部钩子函数,用于判断用户名是否已存在,只能判断一个字段
    # 函数名称clean_username中的username必须与form中username一致
    def clean_username(self):
        name = self.cleaned_data.get("username")
        res = models.UserInfo.objects.filter(username=name).first()
        if res:
            raise ValidationError("用户名已存在")
        return name

    # 全局钩子,用来判断两次密码是否一致,能判断所有字段
    def clean(self):
        pwd = self.cleaned_data.get("password")
        re_pwd = self.cleaned_data.get("re_password")
        if pwd != re_pwd:
            raise ValidationError("两次密码不一致")
        return self.cleaned_data
