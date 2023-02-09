from django.urls import path

from .views import customer,index, login, register, reset, calendar

urlpatterns = [
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('reset-password', reset, name='reset'),
    path('calendar', calendar, name='calendar'),
    path('customer', customer, name='customer'),
    path('', index, name='index'),
]
