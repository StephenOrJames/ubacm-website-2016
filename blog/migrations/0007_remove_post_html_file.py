# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 20:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20160412_1934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='html_file',
        ),
    ]