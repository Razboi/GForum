# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_post_post_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_views',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
