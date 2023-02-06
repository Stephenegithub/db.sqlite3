from django.contrib import admin
from .models import Customer
from .models import Feedback

# Register your models here.
admin.site.register(Customer)
admin.site.register(Feedback)
