# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-16 00:00
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truck', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='truck',
            name='year',
            field=models.PositiveIntegerField(help_text='Use the following format: YYYY', validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2019)]),
        ),
    ]
