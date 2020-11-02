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

class Appointments(models.Model):
    clientID = models.ForeignKey(Clients, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    settings = (
        (1, ('Face to face')),
        (2, ('Online'))
    )
    setting = models.PositiveSmallIntegerField(
        choices=settings,
        default=1
        )
