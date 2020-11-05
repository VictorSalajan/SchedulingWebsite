from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name="choose_day.html"))),
    path('', views.Change_day.homepage, name='homepage'),
    path('weekly', views.weekly, name='weekly'),
    path('next_day', views.Change_day.next_day, name='next_day'),
    path('previous_day', views.Change_day.previous_day, name='previous_day')
]
