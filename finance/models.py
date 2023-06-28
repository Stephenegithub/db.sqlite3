from django.db import models

from accounts.models import CustomUser
from inventory.models import Cart, Product


# class CakesPayments(models.Model):
#     class Meta:
#         verbose_name = 'Cake Payment'
#         verbose_name_plural = 'Cake Payments'
#
#     PAYMENT_STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]
#     request = models.OneToOneField(product, on_delete=models.CASCADE, related_name='payment')
#     payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='Pending')
#     transaction_id = models.CharField(max_length=100)
#     payment_date = models.DateTimeField(auto_now_add=True)




#
# class Payment(models.Model):
#     class Meta:
#         verbose_name = 'Order Payment'
#         verbose_name_plural = 'Order Payments'
#
#     PAYMENT_STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]
#     cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
#     payment_date = models.DateTimeField(auto_now_add=True)
#     transaction_id = models.CharField(max_length=100)
#     payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='Pending')
#     location = models.CharField(max_length=100, null=True)
#     street_address = models.CharField(max_length=100, null=True)
#
#     def get_location_address(self):
#         if self.location and self.street_address:
#             return f"{self.location}, {self.street_address}"
#         elif self.location:
#             return self.location
#         elif self.street_address:
#             return self.street_address
#         else:
#             return ""


class Account(models.Model):
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.invoice_number}"
