# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 19:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_notification_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='is_liked',
            new_name='is_comment',
        ),
    ]
