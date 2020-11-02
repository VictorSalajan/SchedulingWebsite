from django.shortcuts import render
from django.http import HttpResponse
#from django.contrib.auth.decorators import login_required
from appointments.models import Clients, Appointments
from datetime import datetime
import datetime as date
import calendar

def homepage(request):
    query_set = Appointments.objects.filter(
        datetime__year=datetime.now().year,
        datetime__month=datetime.now().month,
        datetime__day=datetime.now().day
    )
    context = {
        "TodayAppointments": query_set
    }

    return render(request, 'home.html', context)

def weekly(request):
    """ Currently not adapted for weeks that belong to two years """
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    this_week_nr = date.date(year, month, day).isocalendar()[1]
    query_set = Appointments.objects.filter(datetime__week=this_week_nr)
    context = {
        "WeeklyAppointments": query_set
    }
    return render(request, 'weekly.html', context)

# @login_required
# def index(request):
#     return render(request, 'appointments/index')
