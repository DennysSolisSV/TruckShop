# Generated by Django 2.1.7 on 2019-03-31 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_orders', '0015_workorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='time_labor',
            field=models.DecimalField(decimal_places=2, max_digits=100),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='status',
            field=models.CharField(choices=[('quotes', 'Quotes'), ('dropped_off', 'Dropped Off'), ('in_process', 'In Process'), ('closed', 'Closed Work Order'), ('paid', 'Paid Work Order')], default='quotes', max_length=150),
        ),
    ]