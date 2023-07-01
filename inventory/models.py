import importlib

from django.db import models
from djmoney.models.fields import MoneyField

from accounts.models import CustomUser


# cart

# class Category(models.Model):
#     class Meta:
#         verbose_name = 'Category'
#         verbose_name_plural = 'Categories'
#
#     name = models.CharField(max_length=250, unique=True)
    # installation_cost = MoneyField(max_digits=10, decimal_places=2, default_currency='KES',
    #                                verbose_name='Installation Price', null=True)
    # design_cost = MoneyField(max_digits=10, decimal_places=2, default_currency='KES',
    #                          verbose_name='Design Price', null=True)
    #
    # def __str__(self):
    #     return self.name


# class Service(models.Model):
#     class Meta:
#         verbose_name = 'Service Request'
#         verbose_name_plural = 'Service RequestS'

#     INSTALLATION = 'Installation'
#     DESIGN = 'Design'
#     SERVICE_CHOICES = [
#         # (INSTALLATION_ONLY, 'Installation Only'),
#         (INSTALLATION, 'Installation'),
#         (DESIGN, 'Design'),
#     ]

#     name = models.CharField(max_length=10)
#     image = models.ImageField(upload_to='products/', null=True)
#     installation_cost = MoneyField(max_digits=10, decimal_places=2, default_currency='KES', verbose_name='Installation Price', null=True)
#     description = models.TextField(max_length=255)
#     service_type = models.CharField(max_length=255, choices=SERVICE_CHOICES, default=DESIGN)


class Cart(models.Model):
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', through='CartItem')
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    pickup_station = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        module_name = 'shipping.models'
        module = importlib.import_module(module_name)
        UserPickUpStation = getattr(module, 'UserPickUpStation')
        self.pickup_station = models.ForeignKey(UserPickUpStation, on_delete=models.CASCADE, null=True)

    @property
    def total_cost(self):
        if self.cartitem_set.first() and self.cartitem_set.first().service == CartItem.DESIGN_AND_INSTALLATION:
            cart_items = self.cartitem_set.all()
            product_prices = [item.subtotal for item in cart_items]
            product_price = sum(product_prices)
            return product_price

        elif self.cartitem_set.first() and self.cartitem_set.first().service == CartItem.DESIGN_ONLY:
            cart_items = self.cartitem_set.all()
            product_prices = [item.subtotal for item in cart_items]
            product_price = sum(product_prices)
            return product_price

        else:
            cart_items = self.cartitem_set.all()
            installation_cost = sum([item.product.installation_cost.amount for item in cart_items if
                                     item.product and item.product.installation_cost])
            installation_cost = 0 if installation_cost and self.cartitem_set.first() and self.cartitem_set.first().service == CartItem.DESIGN_ONLY else installation_cost  # set installation cost to 0 for design only
            product_prices = [item.subtotal for item in cart_items]
            product_price = sum(product_prices)
            return product_price + installation_cost

    @classmethod
    def get_valid_service_types(cls):
        return [choice[0] for choice in CartItem.SERVICE_CHOICES]

    def get_driver(self):
        if self.driver:
            return self.driver.get_user_type_display()
        return ''


class CartItem(models.Model):
    # INSTALLATION_ONLY = 'Installation Only'
    DESIGN_AND_INSTALLATION = 'Design and Installation'
    DESIGN_ONLY = 'Design Only'
    SERVICE_CHOICES = [
        # (INSTALLATION_ONLY, 'Installation Only'),
        (DESIGN_AND_INSTALLATION, 'Design and Installation'),
        (DESIGN_ONLY, 'Design Only'),
    ]

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    service = models.CharField(max_length=255, choices=SERVICE_CHOICES, default=DESIGN_ONLY)
    quantity = models.PositiveIntegerField(default=0)

    @property
    def subtotal(self):
        price = self.product.price
        installation_cost = self.product.installation_cost

        if self.service == CartItem.DESIGN_ONLY:
            return price.amount * self.quantity
        else:
            return (price.amount + installation_cost.amount) * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart for {self.cart.user.username}"

    def total_cost(self):
        return self.product.total_cost(self.service) * self.quantity


class Product(models.Model):
    class Meta:
        verbose_name = 'Products in stock'

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='KES', verbose_name='Design Price')
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.PositiveIntegerField(null=True, verbose_name='Quantity in stock')

    # def __str__(self):
    #     return self.name
    #
    # def total_cost(self, service):
    #     price = self.price.amount
    #     installation_cost = self.installation_cost.amount if self.installation_cost else 0
    #
    #     if service == CartItem.DESIGN_ONLY:
    #         return price
    #     elif service == CartItem.INSTALLATION_ONLY:
    #         return installation_cost
    #     else:
    #         return price + installation_cost
    #
    # @staticmethod
    # def search(name):
    #     return Product.objects.filter(name__icontains=name)


