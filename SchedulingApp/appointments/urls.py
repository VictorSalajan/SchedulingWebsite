from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('/weekly', views.weekly, name='weekly')
]
