# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-26 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0017_remove_post_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(null=True),
        ),
    ]
