from django.db import models
#from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=64)
    problem = models.CharField(max_length=64)
    notes = models.CharField(max_length=1000)
    session_number = models.IntegerField()  # to implement auto-increment in views
    recurring = models.BooleanField()
    price = models.IntegerField()
    receipt = models.BooleanField()
    email = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name} - {self.problem}'

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    datetime = models.DateTimeField()   # another name
    SETTINGS = (
        (1, ('Face to face')),
        (2, ('Online'))
    )
    setting = models.PositiveSmallIntegerField(
        choices=SETTINGS,
        default=1
        )

    def __str__(self):
        eventdate = self.datetime.strftime("%m/%d/%Y, %H:%M")
        eventdate = datetime.strptime(eventdate, "%m/%d/%Y, %H:%M")
        return f'{str(eventdate)[:-3]} - {self.client.__str__()} -- User: {self.user}'
