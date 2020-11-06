from django.shortcuts import render
from appointments.models import Clients, Appointments
from datetime import datetime, date, timedelta, time
import calendar
from django.utils import timezone
from django.contrib.auth.decorators import login_required


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

def get_query_set_and_intervals(query_set):
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

@login_required
def weekly(request):
    """ Currently not adapted for weeks that belong to two years """
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    this_week_nr = date(year, month, day).isocalendar()[1]
    query_set = Appointments.objects.filter(datetime__week=this_week_nr)
    query_set = query_set.order_by('datetime')

    while now.isocalendar()[2]  > 1:
        now -= timedelta(days=1)

    day_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    dates = []
    for i in range(5):
        dates.append([day_labels[i], calendar.month_name[now.month][:3], now.day])
        now += timedelta(days=1)
    
    query_set_and_intervals = get_query_set_and_intervals(query_set)

    context = {
        "WeeklyAppointments": query_set_and_intervals,#query_set,
        "dates": dates,
    }
    return render(request, 'weekly.html', context)