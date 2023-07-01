from django.contrib import admin

from products.models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'category', 'quantity', 'price', 'image', 'created_at', 'updated_at')
    list_filter = ('name', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('name', 'description', 'category')


admin.site.register(Product)
admin.site.register(Category)
