# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-24 12:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_forum_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='slug',
            field=models.SlugField(blank=True, max_length=170, null=True),
        ),
    ]
