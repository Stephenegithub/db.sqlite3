# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Your other URL patterns...
    path('create-invoice/', views.create_invoice, name='create_invoice'),
]
