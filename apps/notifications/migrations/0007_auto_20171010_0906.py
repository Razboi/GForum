# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-10 09:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_auto_20171009_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_comment', to='comments.Comment'),
        ),
    ]
