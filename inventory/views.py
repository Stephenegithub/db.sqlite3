from django.shortcuts import render, redirect
from django.views import View
from products.models import Product
from .forms import OrderForm, AddToCartForm
from .models import Order


class ProductView(View):
    def get(self, request):
        products = Product.objects.all()
        context = {'products': products}
        return render(request, 'customer/products.html', context)


def add_to_cart(request):
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            # Process the form data and perform additional actions
            product_name = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']
            shipping_address = form.cleaned_data['shipping_address']

            # Example: Print the cart details
            return render(request, 'cart/cart_details.html', {
                'product_name': product_name,
                'quantity': quantity,
                'price': price,
                'shipping_address': shipping_address
            })
    else:
        form = AddToCartForm()

    return render(request, 'cart/add_to_cart.html', {'form': form})


def creatorder(request):
    return render(request, 'inventory/createorder.html')
