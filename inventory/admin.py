from django.contrib import admin
from .models import Product, Cart


# Register your models here.

# admin.site.register(Product)
admin.site.register(Cart)


@admin.register(Product)
class ProductModel(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    list_filter = ('name', 'description')


# @admin.register(Cart)
# class CartModel(admin.ModelAdmin):
#     list_filter = ('customer', 'products')
#     list_display = ('customer', 'products', 'quantity',)
