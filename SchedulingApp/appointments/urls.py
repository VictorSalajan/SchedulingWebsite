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
    path('register', views.register, name='register')
]
