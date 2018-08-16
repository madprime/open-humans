# Generated by Django 2.1 on 2018-08-13 21:47

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_import', '0006_remove_datafile_archived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datafile',
            name='metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]