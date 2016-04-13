# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-13 15:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20160413_0102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='template',
        ),
        migrations.AddField(
            model_name='post',
            name='html_file',
            field=models.FileField(null=True, upload_to='blog/html/'),
        ),
    ]
