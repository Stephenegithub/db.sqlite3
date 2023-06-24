# from django.db import models
#
#
# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='products_images')
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     inventory = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.name
#
#     def decrease_inventory(self, quantity):
#         self.inventory -= quantity
#         self.save()


from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('eggs', 'Eggs'),
        ('cakes', 'Cakes'),
        ('chicken', 'Chicken'),
    )

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products_images')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    inventory = models.IntegerField(default=0)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

    def decrease_inventory(self, quantity):
        self.inventory -= quantity
        self.save()
