# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-26 09:22
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0009_auto_20170927_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]
