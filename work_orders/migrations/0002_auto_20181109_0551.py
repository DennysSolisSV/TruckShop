# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-09 05:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work_orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mechachictimetask',
            name='task',
        ),
        migrations.RemoveField(
            model_name='mechachictimetask',
            name='user',
        ),
        migrations.DeleteModel(
            name='MechachicTimeTask',
        ),
    ]