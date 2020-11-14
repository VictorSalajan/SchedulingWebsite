from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('daily', views.daily, name='daily'),
    path('weekly', views.weekly, name='weekly'),
    path('next_day', views.next_day, name='next_day'),
    path('previous_day', views.previous_day, name='previous_day'),
    path('previous_week', views.previous_week, name='previous_week'),
    path('next_week', views.next_week, name='next_week'),
    path('<int:pk>/detailed_view', views.detailed_view, name='detailed_view'),
    path('clients', views.clients, name='clients'),
    path('<int:pk>edit_appointment', views.edit_appointment, name='edit_appointment'),
    path('add_client', views.add_client, name='add_client'),
    path('appointments', views.appointments, name='appointments'),
    path('add_appointment', views.add_appointment, name='add_appointment'),
    path('delete_appointment', views.delete_appointment, name='delete_appointment'),
    path('register', views.register, name='register')
]
