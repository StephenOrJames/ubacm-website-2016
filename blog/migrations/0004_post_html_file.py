# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-09 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_identity'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='html_file',
            field=models.FileField(null=True, upload_to='blogposts/'),
        ),
    ]
