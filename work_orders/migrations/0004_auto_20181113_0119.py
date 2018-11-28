# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-13 01:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('work_orders', '0003_mechachictimetask'),
    ]

    operations = [
        migrations.CreateModel(
            name='MechanicTimeDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('clock_in', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='mechanictime',
            name='task',
        ),
        migrations.RemoveField(
            model_name='mechanictime',
            name='user',
        ),
        migrations.DeleteModel(
            name='MechanicTime',
        ),
    ]