# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-26 18:32
from __future__ import unicode_literals

from django.db import migrations
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_auto_20171026_0725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=martor.models.MartorField(),
        ),
    ]