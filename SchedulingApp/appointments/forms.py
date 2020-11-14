from django import forms
from .models import Client, Appointment

class AddClient(forms.Form):
    name = forms.CharField(label="Name", max_length=64)
    problem = forms.CharField(label="Problem", max_length=64)
    session_number = forms.IntegerField(label="Session Number", required=False)
    recurring = forms.BooleanField(label="Recurring", required=False)
    email = forms.CharField(label="Email", required=False, max_length=64)

class AddAppointment(forms.Form):
    client = forms.ChoiceField(label="Choose Client", choices=Client.objects.all())
    event_date = forms.DateTimeField(label="Date & Time")
    SETTINGS = (
        (1, ('Face to face')),
        (2, ('Online'))
    )
    setting = forms.ChoiceField(label="Setting", choices=SETTINGS)
    notes = forms.CharField(label="Notes", max_length=1000)
    price = forms.IntegerField(label="Price")
    receipt = forms.BooleanField(label="Receipt")
