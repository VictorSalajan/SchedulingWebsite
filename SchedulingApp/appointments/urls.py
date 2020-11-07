from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('daily', views.Change_day.daily, name='daily'),
    path('weekly', views.Change_week.weekly, name='weekly'),
    path('next_day', views.Change_day.next_day, name='next_day'),
    path('previous_day', views.Change_day.previous_day, name='previous_day'),
    path('previous_week', views.Change_week.previous_week, name='previous_week'),
    path('next_week', views.Change_week.next_week, name='next_week'),
    path('register', views.register, name='register')
]
