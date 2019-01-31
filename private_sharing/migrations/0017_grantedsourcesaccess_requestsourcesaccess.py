# Generated by Django 2.1.5 on 2019-01-30 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('private_sharing', '0016_auto_20190128_2111'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrantedSourcesAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('project_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='private_sharing.DataRequestProjectMember')),
                ('requested_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='granted_requested_project', to='private_sharing.DataRequestProject')),
                ('requesting_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='granted_requesting_project', to='private_sharing.DataRequestProject')),
            ],
        ),
        migrations.CreateModel(
            name='RequestSourcesAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('requested_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_project', to='private_sharing.DataRequestProject')),
                ('requesting_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requesting_project', to='private_sharing.DataRequestProject')),
            ],
        ),
    ]
