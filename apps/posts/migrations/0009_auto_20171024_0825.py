# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-24 08:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20171023_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='name',
            field=models.TextField(),
        ),
    ]
