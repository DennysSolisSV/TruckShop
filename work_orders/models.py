from decimal import Decimal
from django.db import models
from django.db.models import Sum
from django.db.models import Q
from django.db.models.signals import pre_save, post_save, post_delete
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
    total_parts = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2)
    total_labor = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2)
    total_task = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2)

    objects = TaskManager()

    def __str__(self):
        return self.title + " - " + str(self.work_order.number_order)

    def get_absolute_url(self):
        return reverse("work_orders:task_detail", kwargs={"pk": self.pk})


def pre_save_task_receiver(sender, instance, *args, **kwargs):
    instance.total_parts = get_sum_total_parts_in_task(instance)
    instance.total_labor = Decimal(instance.time_labor) * Decimal(115.00)
    instance.total_task = instance.total_parts + instance.total_labor


pre_save.connect(pre_save_task_receiver, sender=Task)


class PartsByTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    part = models.ForeignKey(Part)
    quantity = models.IntegerField()
    price = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2)
    subtotal = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2)
    operation = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.part)


def pre_save_partsbytask_receiver(sender, instance, *args, **kwargs):
    if instance.quantity > 0:
        instance.subtotal = instance.quantity * instance.part.price
        instance.price = instance.part.price

        part = Part.objects.get(id=instance.part.id)

        # add or remove to the available in part for add and update
        if instance.operation == "Add":
            part.available = part.available - instance.quantity

        if instance.operation == "Update":
            partbytask = PartsByTask.objects.get(id=instance.id)

            print("old:" + str(partbytask.quantity))
            print("new:" + str(instance.quantity))
            if partbytask.quantity > instance.quantity:
                part.available = part.available + \
                    (partbytask.quantity - instance.quantity)
            elif partbytask.quantity < instance.quantity:
                part.available = part.available - \
                    (instance.quantity - partbytask.quantity)

        part.save()
        print(part.available)
    else:
        instance.subtotal = 0.00


pre_save.connect(pre_save_partsbytask_receiver, sender=PartsByTask)


# update totals in task after delete part and part.available
def post_delete_partsbytask_receiver(sender, instance, *args, **kwargs):
    qs = Task.objects.get(id=instance.task.id)
    part = Part.objects.get(id=instance.part.id)

    qs.total_parts = get_sum_total_parts_in_task(qs)
    qs.total_labor = Decimal(qs.time_labor) * Decimal(115.00)
    qs.total_task = qs.total_parts + qs.total_labor
    qs.save()

    part.available = part.available + instance.quantity
    part.save()
    print(part.available)


post_delete.connect(post_delete_partsbytask_receiver, sender=PartsByTask)

# update totals in task after save


def post_save_partsbytask_receiver(sender, instance, *args, **kwargs):
    qs = Task.objects.get(pk=instance.task.pk)
    qs.total_parts = get_sum_total_parts_in_task(qs)
    qs.total_labor = Decimal(qs.time_labor) * Decimal(115.00)
    qs.total_task = qs.total_parts + qs.total_labor
    qs.save()


post_save.connect(post_save_partsbytask_receiver, sender=PartsByTask)


class MechachicTimeTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now=True)
    clock_in = models.BooleanField()


def get_sum_total_parts_in_task(instance):
    parts = PartsByTask.objects.filter(task=instance)
    if parts:
        out = parts.aggregate(Sum('subtotal'))
        return out["subtotal__sum"]
    else:
        return Decimal(0)
