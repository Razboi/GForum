# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-13 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]