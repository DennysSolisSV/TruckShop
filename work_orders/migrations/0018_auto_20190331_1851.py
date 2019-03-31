# Generated by Django 2.1.7 on 2019-03-31 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_orders', '0017_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('No assigned', 'no_assigned'), ('In process', 'in_process'), ('Completed', 'completed')], default='no_assigned', max_length=150),
        ),
    ]