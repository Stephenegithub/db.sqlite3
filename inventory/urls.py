from django.urls import path
from .views import *

app_name = 'inventory'
urlpatterns = [
    path('products', ProductView.as_view(), name="product-view"),

]
