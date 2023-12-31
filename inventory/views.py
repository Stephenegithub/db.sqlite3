from django.shortcuts import render
from django.views import View
from products.models import Product


class ProductView(View):
    def get(self, request):
        products = Product.objects.all()
        context = {'products': products}
        return render(request, 'customer/products.html', context)


def inventory(request):
    return render(request, 'inventory/index.html')


def stock_out(request):
    return render(request, 'inventory/out_of_stock.html')
