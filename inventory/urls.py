from django.urls import path

from products import views
from products.views import product_list
from .views import *

app_name = 'inventory'
urlpatterns = [
    path('products', ProductView.as_view(), name="product-view"),
    path('inventory', inventory, name='index'),
    path('products/', product_list, name='product_list'),
    path('inventory', stock_out, name='stock_out'),
    path('add/', views.add_product, name='add_product'),
    path('update/<int:product_id>/', views.update_product, name='update_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
]



