from django.db import models
#from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=64)
    session_number = models.IntegerField()  # to implement auto-increment in views
    email = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    event_date = models.DateTimeField()
    SETTINGS = (
        (1, ('Face to face')),
        (2, ('Online'))
    )
    setting = models.PositiveSmallIntegerField(
        choices=SETTINGS,
        default=1
        )
    problem = models.CharField(max_length=64, null=True, blank=True)
    notes = models.CharField(max_length=1000, null=True, blank=True)
    recurring = models.BooleanField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    receipt = models.BooleanField(null=True, blank=True)

    def __str__(self):
        eventdate = self.event_date.strftime("%m/%d/%Y, %H:%M")
        eventdate = datetime.strptime(eventdate, "%m/%d/%Y, %H:%M")
        return f'{str(eventdate)[:-3]} - {self.client.__str__()} - {self.problem} -- User: {self.user}'
