# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-07-09 22:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('open_humans', '0010_auto_20180611_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image_url',
            field=models.CharField(blank=True, max_length=2083),
        ),
    ]