# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-26 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0011_auto_20171026_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(),
        ),
    ]
