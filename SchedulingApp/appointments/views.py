from django.shortcuts import render, redirect
from appointments.models import Clients, Appointments
from datetime import datetime, date, timedelta, time
import calendar
from django.utils import timezone
#from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def register(response):
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect('')
    else:
        form = UserCreationForm()

    return render(response, 'register.html', {"form": form})

def get_query_set_and_intervals(query_set):
    """ For both daily & weekly views """
    query_set_and_intervals = []
    for _, obj in enumerate(query_set):
        start = obj.datetime.time()
        end = datetime.combine(
                        date.today(), 
                        time(obj.datetime.time().hour, obj.datetime.time().minute)
                        ) + timedelta(minutes=50)
        end = end.time()
        query_set_and_intervals.append([obj, f'{str(start)[:5]} - {str(end)[:5]}'])
    return query_set_and_intervals

class Change_day:
    current_date = datetime.now()

    @staticmethod
    def query_set_and_context():
        year = Change_day.current_date.year
        month = Change_day.current_date.month
        day = Change_day.current_date.day
        query_set = Appointments.objects.filter(
            datetime__year=year,
            datetime__month=month,
            datetime__day=day
        )
        current_week = date(year, month, day).isocalendar()
        week_day = calendar.day_name[current_week[2] - 1]
        month = calendar.month_name[int(Change_day.current_date.month)][:3]
        day = Change_day.current_date.day
        current_date = f'{month}. {day}, {Change_day.current_date.year}'
        query_set_and_intervals = get_query_set_and_intervals(query_set)
        context = {
            "DailyAppointments": query_set_and_intervals,
            "current_date": current_date,
            "week_day": week_day
        }
        return context

    @staticmethod
    def homepage(request):
        Change_day.current_date = datetime.now()

        context = Change_day.query_set_and_context()
        return render(request, 'choose_day.html', context)

    @staticmethod
    def previous_day(request):
        Change_day.current_date -= timedelta(days=1)

        context = Change_day.query_set_and_context()
        return render(request, 'choose_day.html', context)

    @staticmethod
    def next_day(request):
        Change_day.current_date += timedelta(days=1)

        context = Change_day.query_set_and_context()
        return render(request, 'choose_day.html', context)

class Change_week:
    now = datetime.now()

    @staticmethod
    def query_set_and_context(now):
        current_week = date(now.year, now.month, now.day).isocalendar()[1]
        query_set = Appointments.objects.filter(datetime__week=current_week)
        query_set = query_set.order_by('datetime')

        while now.isocalendar()[2]  > 1:
            now -= timedelta(days=1)

        day_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        no_appointments = []
        for i in range(5):
            if len(query_set.filter(datetime__day=now.day, datetime__month=now.month, datetime__year=now.year)) == 0:
                no_appointments.append(True)
            else:
                no_appointments.append(False)
        
        dates = []
        for i in range(5):
            dates.append([day_labels[i], calendar.month_name[now.month][:3], now.day])
            now += timedelta(days=1)

        query_set_and_intervals = get_query_set_and_intervals(query_set)

        context = {
            "WeeklyAppointments": query_set_and_intervals,
            "dates": dates,
            "no_appointments": no_appointments
        }
        return context

    @staticmethod
    def weekly(request):
        """ Currently not adapted for weeks that belong to two years """
        Change_week.now = datetime.now()
        now = Change_week.now
        context = Change_week.query_set_and_context(now)

        return render(request, 'weekly.html', context)

    @staticmethod
    def previous_week(request):
        Change_week.now -= timedelta(days=7)
        context = Change_week.query_set_and_context(Change_week.now)
        
        return render(request, 'weekly.html', context)

    @staticmethod
    def next_week(request):
        Change_week.now += timedelta(days=7)
        context = Change_week.query_set_and_context(Change_week.now)
        
        return render(request, 'weekly.html', context)