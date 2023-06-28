from django.shortcuts import render, redirect

from products.models import Product


def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    if product.inventory > 0:
        product.decrease_inventory(1)
        # Perform any additional logic here, e.g., add the product to the customer's cart
        return redirect('product_list')
    else:
        return render(request, 'inventory/out_of_stock.html')


def product_list(request):
    products = Product.objects.all()
    categories = Product.CATEGORY_CHOICES
    return render(request, 'inventory/product_list.html', {'products': products, 'categories': categories})
