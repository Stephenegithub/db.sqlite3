from django.urls import path
from .views import *

app_name = 'inventory'
urlpatterns = [
    path('products', ProductView.as_view(), name="product-view"),
    path('inventory', add_to_cart, name="add_to_cart"),
    path('inventory', creatorder, name="creatorder")
]
