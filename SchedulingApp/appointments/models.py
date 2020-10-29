from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)

class Clients(models.Model):
    name = models.CharField(max_length=64)
    problem = models.CharField(max_length=64)
    notes = models.CharField(max_length=1000)
    session_number = models.IntegerField()
    recurring = models.BooleanField()
    price = models.IntegerField()
    receipt = models.BooleanField()
    email = models.CharField(max_length=64)
