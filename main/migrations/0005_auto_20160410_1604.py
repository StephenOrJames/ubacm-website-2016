# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-10 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20160408_2030'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackgroundImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='homepage/background/')),
            ],
            options={
                'db_table': 'backgroundImages',
            },
        ),
        migrations.AlterModelOptions(
            name='contactform',
            options={'ordering': ['-sent_at'], 'verbose_name_plural': 'Contact Page Form'},
        ),
    ]
