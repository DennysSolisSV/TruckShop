from django.db import models


class Part(models.Model):
    part_number = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    price = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    cost = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    existence = models.IntegerField()
    available = models.IntegerField()

    def __str__(self):
        return self.part_number
