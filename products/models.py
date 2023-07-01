from django.db import models
from djmoney.models.fields import MoneyField

from accounts.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    class Meta:
        verbose_name = 'Products in stock'

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='KES', verbose_name='Design Price')
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.PositiveIntegerField(null=True, verbose_name='Quantity in stock')

    def __str__(self):
        return self.name


    @staticmethod
    def search(name):
        return Product.objects.filter(name__icontains=name)
