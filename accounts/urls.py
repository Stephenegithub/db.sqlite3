from django.urls import path
from .views import customer, index, reset, calendar, UserCreateView, login, icons, profile, product, order

app_name = "accounts"

urlpatterns = [
    path('', login, name='login'),
    path('register/', UserCreateView.as_view(), name="register"),
    path('reset-password', reset, name='reset'),
    path('calendar', calendar, name='calendar'),
    path('icons', icons, name='icons'),
    path('profile', profile, name='profile'),
    path('customer', customer, name='customer'),
    path('index', index, name='index'),
    path('products', product, name='product'),
    path('orders', order, name='order'),
]
