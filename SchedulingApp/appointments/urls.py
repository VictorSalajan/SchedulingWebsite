from django.urls import path
from . import views
#from django.contrib.auth.decorators import login_required
#from django.views.generic import TemplateView

urlpatterns = [
#    path('', login_required(TemplateView.as_view(template_name="choose_day.html"))),
    path('', views.Change_day.homepage, name='homepage'),
    path('weekly', views.Change_week.weekly, name='weekly'),
    path('next_day', views.Change_day.next_day, name='next_day'),
    path('previous_day', views.Change_day.previous_day, name='previous_day'),
    path('previous_week', views.Change_week.previous_week, name='previous_week'),
    path('next_week', views.Change_week.next_week, name='next_week'),
    path('register', views.register, name='register')
]
