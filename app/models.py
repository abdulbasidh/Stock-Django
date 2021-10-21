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

class Products(models.Model):
    product_id = models.CharField(max_length=10)
    prod_name = models.CharField(max_length=50)
    qty = models.IntegerField()
    tot_price = models.IntegerField()
    seller = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'products'

class Supplier(models.Model):
    supplier_id = models.CharField(max_length=10)
    sup_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    phone = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'supplier'
