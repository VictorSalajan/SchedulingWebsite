from django.shortcuts import render, redirect
from appointments.models import Client, Appointment
from datetime import datetime, date, timedelta, time
import calendar
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login, authenticate

def register(request):
    if request.user.is_authenticated:
        return redirect('/daily')
    if request.method == "POST":    #
        form = UserCreationForm(request.POST)   #
        if form.is_valid():
            form.save()
        return redirect('homepage')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {"form": form})     #

def homepage(request):
    if request.user.is_authenticated:
        return redirect('/daily')
    else:
        return redirect('/accounts/login/')

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
    def query_set_and_context(request):
        current_date = request.session.get('current_date')
        current_date = datetime.strptime(current_date, "%m/%d/%Y")
        year = current_date.year
        month = current_date.month
        day = current_date.day
        query_set = Appointment.objects.filter(
            datetime__year=year,
            datetime__month=month,
            datetime__day=day,
            user = request.user
        )
        current_week = date(year, month, day).isocalendar()
        week_day = calendar.day_name[current_week[2] - 1]
        month = calendar.month_name[int(current_date.month)][:3]
        day = current_date.day
        current_date = f'{month}. {day}, {current_date.year}'
        query_set_and_intervals = get_query_set_and_intervals(query_set)
        context = {
            "DailyAppointments": query_set_and_intervals,
            "current_date": current_date,
            "week_day": week_day
        }
        return context

    @staticmethod
    def daily(request):
        current_date = datetime.now().strftime("%m/%d/%Y")
        request.session['current_date'] = current_date

        context = Change_day.query_set_and_context(request)
        return render(request, 'choose_day.html', context)

    @staticmethod
    def previous_day(request):
        current_date = request.session.get('current_date', \
            datetime.now().strftime("%m/%d/%Y"))
        current_date = datetime.strptime(current_date, "%m/%d/%Y") - timedelta(days=1)
        request.session['current_date'] = current_date.strftime("%m/%d/%Y")

        context = Change_day.query_set_and_context(request)
        return render(request, 'choose_day.html', context)

    @staticmethod
    def next_day(request):
        current_date = request.session.get('current_date', \
            datetime.now().strftime("%m/%d/%Y"))
        current_date = datetime.strptime(current_date, "%m/%d/%Y") + timedelta(days=1)
        request.session['current_date'] = current_date.strftime("%m/%d/%Y")

        context = Change_day.query_set_and_context(request)
        return render(request, 'choose_day.html', context)

class Change_week:
    now = datetime.now()    # store in request.session

    @staticmethod
    def query_set_and_context(now):
        current_week = date(now.year, now.month, now.day).isocalendar()[1]
        query_set = Appointment.objects.filter(datetime__week=current_week)
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
        now = Change_week.now   #now=request.session.get(now)
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