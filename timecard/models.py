from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class TimeDay(models.Model):
    user = models.ForeignKey(User, on_delete='CASCADE')
    time = models.DateTimeField(auto_now_add=True)
    clock_in = models.BooleanField()
