from django.shortcuts import render
from django.http import HttpResponse
#from django.contrib.auth.decorators import login_required
from appointments.models import Clients, Appointments
from datetime import datetime
import datetime as date
import calendar
from django.utils import timezone

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

class Change_day:
    current_date = datetime.now()
    
    @staticmethod
    def construct_query_set():
        year = Change_day.current_date.year
        month = Change_day.current_date.month
        day = Change_day.current_date.day
        query_set = Appointments.objects.filter(
            datetime__year=year,
            datetime__month=month,
            datetime__day=day
        )
        return query_set

    @staticmethod    
    def previous_day(request):
        Change_day.current_date -= date.timedelta(days=1)
        month = Change_day.current_date.month
        day = Change_day.current_date.day
        no_appointments = f'{calendar.month_name[int(month)]} {day}'
        context = {
            "CurrentDay": Change_day.construct_query_set(),
            "DayWithoutAppointments": no_appointments
        }
        return render(request, 'previous_day.html', context)

    @staticmethod
    def next_day(request):
        Change_day.current_date += date.timedelta(days=1)
        month = Change_day.current_date.month
        day = Change_day.current_date.day
        no_appointments = f'{calendar.month_name[int(month)]} {day}'
        context = {
            "CurrentDay": Change_day.construct_query_set(),
            "DayWithoutAppointments": no_appointments
        }
        return render(request, 'next_day.html', context)

def weekly(request):
    """ Currently not adapted for weeks that belong to two years """
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    this_week_nr = date.date(year, month, day).isocalendar()[1]
    query_set = Appointments.objects.filter(datetime__week=this_week_nr)
    query_set = query_set.order_by('datetime')

    while now.isocalendar()[2]  > 1:
        now -= date.timedelta(days=1)

    day_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    dates = []
    for i in range(5):
        dates.append([day_labels[i], calendar.month_name[now.month][:3], now.day])
        now += date.timedelta(days=1)
    
    context = {
        "WeeklyAppointments": query_set,
        "dates": dates
    }
    return render(request, 'weekly.html', context)

# @login_required
# def index(request):
#     return render(request, 'appointments/index')
