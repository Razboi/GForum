# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 12:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0006_auto_20170921_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='identifier',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
