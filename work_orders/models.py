from django.db import models
from django.conf import settings
from accounts.models import Client
from truck.models import Truck
from inventory.models import Part


class WorkOrder(models.Model):
    number_order = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number_order) + " -  - " + str(self.client)


class Task(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    time_labor = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    mechanic = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class PartsByTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.part


class MechachicTimeTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    type_time = models.CharField(max_length=15)


class MechanicTime(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    type_time = models.CharField(max_length=15)
