from django.urls import path
from .views import customer, reset, calendar, icons, profile, login_view, UserCreateView

app_name = "accounts"

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', UserCreateView.as_view(), name="register"),
    path('reset-password', reset, name='reset'),
    path('calendar', calendar, name='calendar'),
    path('icons', icons, name='icons'),
    path('profile', profile, name='profile'),
    path('customer', customer, name='customer'),

]
