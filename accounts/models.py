from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        # if not username:
        #     raise ValueError('Users must have a username')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class CustomUser(AbstractUser):
    class UserTypes(models.TextChoices):
        FINANCE = ('FM', 'Finance Manager')
        CUSTOMER = ('CM', 'Customer')
        DRIVER = ('DR', 'Driver')
        INVENTORY = ('IV', 'Inventory Manager')
        SUPPLIER = ('SP', 'Supplier')
        PACKERS = ('PC', 'Packers')
        ADMIN = ('AD', 'Admin')

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, null=True, unique=True)
    user_type = models.CharField(max_length=2, choices=UserTypes.choices, default=UserTypes.CUSTOMER)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        """
        Does the dashboard have a specific permission?
        """
        return self.is_superuser

    def has_module_perms(self, app_label):
        """
        Does the dashboard have permissions to view the app `app_label`?
        """
        return self.is_superuser
