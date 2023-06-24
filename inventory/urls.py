from django.urls import path

from products.views import product_list
from .views import *

app_name = 'inventory'
urlpatterns = [
    path('products', ProductView.as_view(), name="product-view"),
    path('inventory', inventory, name='index'),
    path('products/', product_list, name='product_list'),
    path('inventory', stock_out, name='stock_out')

]
