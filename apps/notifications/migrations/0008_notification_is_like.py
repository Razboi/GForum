# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-10 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0007_auto_20171010_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_like',
            field=models.BooleanField(default=True),
        ),
    ]
