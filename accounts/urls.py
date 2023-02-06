from django.urls import path
from .views import login
from .views import register
from .views import reset
from .views import calendar

urlpatterns = [
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('reset-password', reset, name='reset'),
    path('calendar', calendar, name='calendar'),
]
