from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q
from accounts.models import Client
from truck.models import Truck
from inventory.models import Part

User = settings.AUTH_USER_MODEL


class WorkOrderManager(models.Manager):
    def search(self, query):
        lookups = (
            Q(number_order__icontains=query) |
            Q(client__name__icontains=query) |
            Q(truck__fleet__icontains=query)
        )

        obj = self.get_queryset().filter(lookups).distinct()
        print(obj)
        return obj


class TaskManager(models.Manager):
    def get_by_user(self, request):
        user = request.user
        obj = self.get_queryset().filter(mechanic=user).order_by('work_order', 'id')
        return obj


class WorkOrder(models.Model):
    number_order = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Client)
    truck = models.ForeignKey(Truck)

    objects = WorkOrderManager()

    def __str__(self):
        return str(self.number_order) + " -  - " + str(self.client)

    # def get_absolute_url(self):
    #     return reverse('work_orders:detail', kwargs={'pk': self.id})


class Task(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    time_labor = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2)
    mechanic = models.ForeignKey(User)

    objects = TaskManager()

    def __str__(self):
        return self.title


class PartsByTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    part = models.ForeignKey(Part)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.part)


class MechachicTimeTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now=True)
    clock_in = models.BooleanField()
