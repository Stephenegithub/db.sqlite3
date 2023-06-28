from django.contrib.auth import views as auth_view
from django.urls import path

from .views import customer, reset, calendar, icons, profile, UserCreateView, HomeView

app_name = "accounts"

urlpatterns = [
    path('register/', UserCreateView.as_view(), name="register"),
    path('reset-password', reset, name='reset'),
    path('calendar', calendar, name='calendar'),
    path('icons', icons, name='icons'),
    path('login', auth_view.LoginView.as_view(template_name='login.html'), name="login"),
    path('profile', profile, name='profile'),
    path('customer', customer, name='customer'),
    path('', HomeView.as_view(), name="home-view")
]
