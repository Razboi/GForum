# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-26 07:25
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_auto_20171024_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]
