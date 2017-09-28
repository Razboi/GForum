# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 09:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20170927_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='score',
            field=models.ManyToManyField(blank=True, null=True, related_name='post_score', to=settings.AUTH_USER_MODEL),
        ),
    ]
