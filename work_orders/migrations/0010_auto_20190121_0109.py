# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-21 01:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_orders', '0009_partsbytask_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='total_labor',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
        migrations.AddField(
            model_name='task',
            name='total_parts',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
    ]
