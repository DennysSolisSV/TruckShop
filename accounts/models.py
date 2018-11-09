from django.db import models
from django.contrib import auth


# Create your models here.
# class User(auth.models.User,auth.models.PermissionsMixin):
#
#     def __str__(self):
#         return (self.username)


class Client(models.Model):
    name = models.CharField(max_length=150)
    address = models.TextField()
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    zip_code = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    cs = models.CharField(max_length=150)

    def __str__(self):
        return self.name

#
