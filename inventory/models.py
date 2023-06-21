from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from accounts.models import CustomUser
from products.models import Product


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartProduct')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart for customer {self.customer}'


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


User = get_user_model()

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('stale', 'Stale'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class Order(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='created')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    shipping_address = models.TextField(blank=True, null=True)
    inventory_updated = models.BooleanField(default=False)

    def get_absolute_url(self):
        return f"/orders/{self.pk}"

    def get_download_url(self):
        return f"/orders/{self.pk}/download/"

    @property
    def is_downloadable(self):
        return bool(self.product)

    def mark_paid(self, custom_amount=None, save=False):
        paid_amount = self.total
        if custom_amount is not None:
            paid_amount = custom_amount
        self.paid = paid_amount
        self.status = 'paid'
        if not self.inventory_updated and self.product:
            self.product.remove_items_from_inventory(count=1, save=True)
            self.inventory_updated = True
        if save:
            self.save()
        return self.paid

    def calculate(self, save=False):
        if not self.product:
            return {}

        subtotal = self.product.price
        tax_rate = Decimal('0.12')
        tax_total = subtotal * tax_rate
        tax_total = tax_total.quantize(Decimal('0.00'))
        total = subtotal + tax_total
        total = total.quantize(Decimal('0.00'))

        totals = {
            "total": total
        }

        for k, v in totals.items():
            setattr(self, k, v)
            if save:
                self.save()

        return totals


def order_pre_save(sender, instance, *args, **kwargs):
    instance.calculate(save=False)


pre_save.connect(order_pre_save, sender=Order)


