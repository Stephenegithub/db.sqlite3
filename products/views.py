from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from products.models import Product
from .forms import ProductForm


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = ProductForm()
    return render(request, 'inventory/add_product.html', {'form': form})


def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    if product.inventory > 0:
        product.decrease_inventory(1)
        # Perform any additional logic here, e.g., add the product to the customer's cart
        return redirect('product_list')
    else:
        return render(request, 'inventory/out_of_stock.html')


def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/update_product.html', {'form': form})


def product_list(request):
    products = Product.objects.all()
    categories = Product.CATEGORY_CHOICES
    return render(request, 'inventory/product_list.html', {'products': products, 'categories': categories})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'inventory/delete_product.html', {'product': product})

# inventory/views.py


# products
class ProductCreateView(CreateView):
    model = Product
    template_name = 'inventory/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('products:add-product')

    def form_valid(self, form):
        # Set the user of the product to the currently logged in user
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        # Add error messages to the form if it is invalid
        messages.error(self.request, 'There was an error with the form. Please try again.')
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        # Set the user of the product to the currently logged in user
        request.POST = request.POST.copy()
        request.POST['user'] = request.user.id
        return super().post(request, *args, **kwargs)