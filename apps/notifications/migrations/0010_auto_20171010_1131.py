# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-10 11:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0009_auto_20171010_1107'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-creation']},
        ),
    ]
