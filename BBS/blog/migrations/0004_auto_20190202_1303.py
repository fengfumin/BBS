# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-02-02 05:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_article_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Comment'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='mobile_phone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
