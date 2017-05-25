from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Business(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)

    def __str__(self):
        return self.username


class Host(models.Model):
    hostname = models.CharField(max_length=32, unique=True)
    address = models.GenericIPAddressField()
    user = models.ManyToManyField(UserInfo)
    business = models.ForeignKey(Business)

    def __str__(self):
        return self.hostname
