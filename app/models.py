from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, UserManager

# Create your models here.

class Users(models.Model):
    email = models.CharField(max_length=60)
    username = models.CharField(max_length=60)
    password = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'users'

class Session(models.Model):
    email = models.CharField(max_length=50)
    token = models.CharField(max_length=64)
    status = models.CharField(max_length=8)
    ip = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'session'
