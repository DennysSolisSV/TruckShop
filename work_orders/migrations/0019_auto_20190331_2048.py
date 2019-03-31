# Generated by Django 2.1.7 on 2019-03-31 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_orders', '0018_auto_20190331_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('no_assigned', 'No assigned'), ('in_process', 'In Process'), ('completed', 'Completed')], default='no_assigned', max_length=150),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='status',
            field=models.CharField(choices=[('quote', 'Quote'), ('dropped_off', 'Dropped Off'), ('in_process', 'In Process'), ('closed', 'Closed Work Order'), ('paid', 'Paid Work Order')], default='quotes', max_length=150),
        ),
    ]
