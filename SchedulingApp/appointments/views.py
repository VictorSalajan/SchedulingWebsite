from django.shortcuts import render, redirect
from django.http import Http404
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
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('homepage')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {"form": form})

def homepage(request):
    if request.user.is_authenticated:
        return redirect('/daily')
    else:
        return redirect('/accounts/login/')

def get_query_set_and_intervals(query_set):
    """ For both daily & weekly views """
    query_set_and_intervals = []
    for _, obj in enumerate(query_set):
        start = obj.event_date.time()
        end = datetime.combine(
                        date.today(), 
                        time(obj.event_date.time().hour, obj.event_date.time().minute)
                        ) + timedelta(minutes=50)
        end = end.time()
        query_set_and_intervals.append([obj, f'{str(start)[:5]} - {str(end)[:5]}'])
    return query_set_and_intervals

def query_set_and_context(request):
    current_date = request.session.get('current_date')
    current_date = datetime.strptime(current_date, "%m/%d/%Y")
    year = current_date.year
    month = current_date.month
    day = current_date.day
    query_set = Appointment.objects.filter(
        event_date__year=year,
        event_date__month=month,
        event_date__day=day,
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

@login_required
def daily(request):
    current_date = datetime.now().strftime("%m/%d/%Y")
    request.session['current_date'] = current_date

    context = query_set_and_context(request)
#####    
    # request.session['daily'] = request.session.get('daily', None)
    # try:
    #     request.session['daily'] = [context['DailyAppointments'][0].id for el in context['DailyAppointments']]
    # except:
    #     pass
#####
    return render(request, 'choose_day.html', context)

@login_required
def previous_day(request):
    current_date = request.session.get('current_date')
    current_date = datetime.strptime(current_date, "%m/%d/%Y") - timedelta(days=1)
    request.session['current_date'] = current_date.strftime("%m/%d/%Y")

    context = query_set_and_context(request)
#####
    # request.session['daily'] = request.session.get('daily', None)
    # try:
    #     request.session['daily'] = [context['DailyAppointments'][0].id for el in context['DailyAppointments']]
    # except:
    #     pass
#####
    return render(request, 'choose_day.html', context)

@login_required
def next_day(request):
    current_date = request.session.get('current_date')
    current_date = datetime.strptime(current_date, "%m/%d/%Y") + timedelta(days=1)
    request.session['current_date'] = current_date.strftime("%m/%d/%Y")

    context = query_set_and_context(request)
#####
    # request.session['daily'] = request.session.get('daily', None)
    # try:
    #     request.session['daily'] = [context['DailyAppointments'][0].id for el in context['DailyAppointments']]
    # except:
    #     pass
#####
    return render(request, 'choose_day.html', context)

def query_set_and_context_week(request):
    current_date = request.session.get('current_date')
    current_date = datetime.strptime(current_date, "%m/%d/%Y")
    current_week = date(
        current_date.year, current_date.month, current_date.day).isocalendar()[1]
    query_set = Appointment.objects.filter(event_date__week=current_week)
    query_set = query_set.order_by('event_date')

    while current_date.isocalendar()[2]  > 1:
        current_date -= timedelta(days=1)

    day_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
    no_appointments = []
    for i in range(5):
        if len(query_set.filter(
            event_date__day=current_date.day, 
            event_date__month=current_date.month, 
            event_date__year=current_date.year)) == 0:
            no_appointments.append(True)
        else:
            no_appointments.append(False)
        
    dates = []
    for i in range(5):
        dates.append(
            [day_labels[i], calendar.month_name[current_date.month][:3], current_date.day])
        current_date += timedelta(days=1)

    query_set_and_intervals = get_query_set_and_intervals(query_set)

    context = {
        "WeeklyAppointments": query_set_and_intervals,
        "dates": dates,
        "no_appointments": no_appointments
    }
    return context

@login_required
def weekly(request):
    current_date = datetime.now().strftime("%m/%d/%Y")
    request.session['current_date'] = current_date

    context = query_set_and_context_week(request)
    return render(request, 'weekly.html', context)

@login_required
def previous_week(request):
    current_date = request.session.get('current_date')
    current_date = datetime.strptime(current_date, "%m/%d/%Y") - timedelta(days=7)
    request.session['current_date'] = current_date.strftime("%m/%d/%Y")
    
    context = query_set_and_context_week(request)
    return render(request, 'weekly.html', context)

@login_required
def next_week(request):
    current_date = request.session.get('current_date')
    current_date = datetime.strptime(current_date, "%m/%d/%Y") + timedelta(days=7)
    request.session['current_date'] = current_date.strftime("%m/%d/%Y")

    context = query_set_and_context_week(request)
    return render(request, 'weekly.html', context)

@login_required
def detailed_view(request, pk):
    # query_set = request.session['daily']
    # new_query_set = []
    # for appointment in query_set:
    #     if appointment == request.user.id:
    #         new_query_set.append(Appointment.id.event_date)
    # context = {
    #     "AppointmentDetails": new_query_set 
    # }
    # return render(request, 'detailed_view.html', context)
    details = Appointment.objects.filter(pk=pk)

    context = {"AppointmentDetails": details}
    return render(request, 'detailed_view.html', context)
