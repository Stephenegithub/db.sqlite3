from django.urls import path

from . import views
from .views import *

app_name = 'products'

urlpatterns = [
    path('add-products/', views.ProductCreateView.as_view(), name='add-product'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    # path('products' add_product, name='add_product'),
]
