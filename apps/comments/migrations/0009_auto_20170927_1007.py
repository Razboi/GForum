# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 10:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0008_comment_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='score',
        ),
        migrations.AddField(
            model_name='comment',
            name='score',
            field=models.ManyToManyField(related_name='comment_score', to=settings.AUTH_USER_MODEL),
        ),
    ]
