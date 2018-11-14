from django.db import models
from django.conf import settings
from accounts.models import Client
from truck.models import Truck
from inventory.models import Part

User = settings.AUTH_USER_MODEL


class TaskQuerySet(models.query.QuerySet):
    def get_by_user(self, user):
        return self.filter(mechanic=user).order_by('work_order', 'id')


class TaskManager(models.Manager):
    def get_queryset(self):  # enlazando el queryset
        return TaskQuerySet(self.model, using=self._db)

    def get_by_user(self, request):
        return self.get_queryset().get_by_user(request.user)


class WorkOrder(models.Model):
    number_order = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Client)
    truck = models.ForeignKey(Truck)

    def __str__(self):
        return str(self.number_order) + " -  - " + str(self.client)


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
