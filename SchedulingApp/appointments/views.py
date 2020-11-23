from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from appointments.models import Client, Appointment
from datetime import datetime, date, timedelta, time
import calendar
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import AddClient, AddAppointment


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
    return render(request, 'choose_day.html', context)

@login_required
def previous_day(request):
    current_date = request.session.get('current_date')
    current_date = datetime.strptime(current_date, "%m/%d/%Y") - timedelta(days=1)
    request.session['current_date'] = current_date.strftime("%m/%d/%Y")

    context = query_set_and_context(request)
    return render(request, 'choose_day.html', context)

@login_required
def next_day(request):
    current_date = request.session.get('current_date')
    current_date = datetime.strptime(current_date, "%m/%d/%Y") + timedelta(days=1)
    request.session['current_date'] = current_date.strftime("%m/%d/%Y")

    context = query_set_and_context(request)
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
    appointment = Appointment.objects.filter(pk=pk)

    context = {"appointment": appointment}
    return render(request, 'detailed_view.html', context)

@login_required
def clients(request):
    clients = Client.objects.all()
    last_appointments_ids = []
    for client in clients:
        try:
            appointments = Appointment.objects.filter(client=client)
            last_appointment = appointments.order_by('event_date').reverse()[0]
            last_appointment_id = last_appointment.id
            last_appointments_ids.append(last_appointment_id)
        except:
            pass
    last_appointments = Appointment.objects.filter(id__in=last_appointments_ids)

    context = {
        "clients": clients,
        "last_appointments": last_appointments
    }
    return render(request, 'clients.html', context)

@login_required
def edit_appointment(request, pk):
    query_set = Appointment.objects.filter(pk=pk)
    appointment = query_set[0]
    if request.method == "POST":
        client = appointment.client
        appointment.event_date = request.POST.get("event_date", str(appointment.event_date))
        appointment.setting = request.POST.get("setting", appointment.setting)
        appointment.client.name = request.POST.get("name", appointment.client.name)
        appointment.client.email = request.POST.get("email", appointment.client.email)
        appointment.client.problem = request.POST.get("problem", appointment.client.problem)
        appointment.notes = request.POST.get('notes', appointment.notes)
        appointment.client.session_number = request.POST.get(
            'session_number', appointment.client.session_number)
        appointment.client.recurring = request.POST.get('recurring', appointment.client.recurring)
        appointment.price = request.POST.get('price', appointment.price)
        appointment.receipt = request.POST.get('receipt', appointment.receipt)

        client.save()
        appointment.save()
        
        return HttpResponseRedirect('/daily')
    return render(request, 'edit_appointment.html', {"appointment": appointment})

@login_required
def add_client(response):
    if response.method == "POST":
        form = AddClient(response.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            problem = form.cleaned_data["problem"]
            session_number = form.cleaned_data["session_number"]
            recurring = form.cleaned_data["recurring"]
            email = form.cleaned_data["email"]
            c = Client(
                name = name,
                problem = problem,
                session_number = session_number,
                recurring = recurring,
                email = email
            )
            c.save()
        return HttpResponseRedirect("/clients")
    else:
        form = AddClient()
    return render(response, 'add_client.html', {"form": form})

@login_required
def add_appointment(response):
    if response.method == "POST":
        form = AddAppointment(response.POST)
        if form.is_valid():
            client = form.cleaned_data["client"]
            event_date = form.cleaned_data["event_date"]
            setting = form.cleaned_data["problem"]
            notes = form.cleaned_data["session_number"]
            price = form.cleaned_data["recurring"]
            receipt = form.cleaned_data["email"]
            a = Appointment(
                client=client,
                event_date=event_date,
                setting=setting,
                notes=notes,
                price=price,
                receipt=receipt
            )
            a.save()
        return HttpResponseRedirect("/clients")
    else:
        form = AddAppointment()
        return render(response, 'add_appointment.html', {"form": form})

    # try:
    #     return render(response, 'add_appointment.html', {"form": form})
    # except:
    #     return HttpResponse('Not yet functional')

@login_required
def delete_appointment(response):
    return HttpResponse('Not yet implemented')
