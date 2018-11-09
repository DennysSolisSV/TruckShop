from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import Client
import datetime


class Truck(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.datetime.now().year)],
        help_text="Use the following format: YYYY")
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    vin = models.CharField(max_length=17)
    license_plate = models.CharField(max_length=10)
    state = models.CharField(max_length=30)
    fleet = models.CharField(max_length=15)
    mileage = models.PositiveIntegerField()

    def __str__(self):
        return self.fleet
