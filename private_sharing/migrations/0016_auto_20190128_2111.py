# Generated by Django 2.1.5 on 2019-01-28 21:11

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('private_sharing', '0015_auto_20190124_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='datarequestprojectmember',
            name='last_authorized',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=32), size=2), default=list, editable=False, size=None),
        ),
        migrations.AddField(
            model_name='datarequestprojectmember',
            name='last_joined',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=32), size=2), default=list, editable=False, size=None),
        ),
    ]
