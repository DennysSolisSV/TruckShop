from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.conf import settings
from django.core.urlresolvers import reverse


from accounts.models import Client
from inventory.models import Part
from truck.models import Truck
from truckshop.utils import unique_work_order_number_generator

User = settings.AUTH_USER_MODEL


class WorkOrderManager(models.Manager):
    # Looking on the different fields
    def search(self, query):
        lookups = (
            Q(number_order__contains=query) |
            Q(client__name__icontains=query) |
            Q(truck__fleet__contains=query)
        )

        obj = self.get_queryset().filter(
            lookups).distinct().order_by('-number_order')
        print(obj)
        return obj

    # Order query from the lastest

    def all(self):
        obj = self.get_queryset().order_by('-number_order')
        return obj


class TaskManager(models.Manager):
    # Getting the tasks that belongs to a user
    def get_by_user(self, request):
        user = request.user
        obj = self.get_queryset().filter(
            mechanic=user).order_by('-number_order', 'id')
        return obj

    # Order query from the lastest

    def all(self, request):
        obj = self.get_queryset.all().order_by('-number_order')
        return obj


class WorkOrder(models.Model):
    number_order = models.PositiveIntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Client)
    truck = models.ForeignKey(Truck)
    slug = models.CharField(max_length=30, null=True, blank=True)

    objects = WorkOrderManager()

    def __str__(self):
        return str(self.number_order) + " -  - " + str(self.client)

    def get_absolute_url(self):
        return reverse("work_orders:detail", kwargs={"slug": self.slug})


def workorder_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.number_order:
        instance.number_order = unique_work_order_number_generator(
            instance)
        instance.slug = str(instance.number_order)


pre_save.connect(workorder_pre_save_receiver, sender=WorkOrder)


class Task(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    time_labor = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2)
    mechanic = models.ForeignKey(User)

    objects = TaskManager()

    def __str__(self):
        return self.title + " - " + str(self.work_order.number_order)

    def get_absolute_url(self):
        return reverse("work_orders:task_detail", kwargs={"pk": self.pk})


class PartsByTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    part = models.ForeignKey(Part)
    quantity = models.IntegerField()
    price = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2)
    subtotal = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2)

    def __str__(self):
        return str(self.part)


def pre_save_partsbytask_receiver(sender, instance, *args, **kwargs):
    if instance.quantity > 0:
        instance.subtotal = instance.quantity * instance.part.price
        instance.price = instance.part.price
    else:
        instance.subtotal = 0.00


pre_save.connect(pre_save_partsbytask_receiver, sender=PartsByTask)


class MechachicTimeTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now=True)
    clock_in = models.BooleanField()
