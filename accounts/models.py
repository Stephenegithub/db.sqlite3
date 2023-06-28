from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

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
        CUSTOMER = 'CM', _('Customer')
        FINANCE = 'FM', _('Finance Manager')
        INVENTORY = 'IV', _('Inventory Manager')
        SUPPLY = 'SP', _('Supplier')
        DRIVER = 'DR', _('Driver')
        PACKERS = 'PC', _('Packers')
        DISPATCH_MANAGER = 'DM', _('Dispatch Manager')
        ADMIN = 'AD', _('Admin')

    user_type = models.CharField(
        _('User Type'),
        max_length=3,
        choices=UserTypes.choices,
        default=UserTypes.CUSTOMER,
    )

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, null=True, unique=True)
    phone_number = models.CharField(max_length=255, null=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def get_user_type_display(self):
        return dict(CustomUser.UserTypes.choices)[self.user_type]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []
    # objects = CustomUserManager()
    #
    # def has_perm(self, perm, obj=None):
    #     """
    #     Does the dashboard have a specific permission?
    #     """
    #     return self.is_superuser
    #
    # def has_module_perms(self, app_label):
    #     """
    #     Does the dashboard have permissions to view the app `app_label`?
    #     """
    #     return self.is_superuser



class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom user model."""

    def create_user(self, email, username, password=None):
        """Creates a user profile object."""

        if not email:
            raise ValueError('Users must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)

        user.user_id = -1
        user.set_password(password)
        user.save(using=self._db)

        return user


class TimeStamp(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Profile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')

    image = models.ImageField(upload_to='Users/profile_pictures/%Y/%m/', default="null")
    phone_number = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(_('Active'), default=False, help_text=_('Activated, users profile is published'))
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    gender = models.CharField(
        max_length=2,
        choices=Gender.choices,
        default=Gender.FEMALE,
    )


class CustomerProfile(Profile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')

    class Meta:
        verbose_name = 'Customer Profile'
        verbose_name_plural = 'Customers Profile'


class FinanceProfile(Profile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='finance_profile')

    class Meta:
        verbose_name = 'Finance Profile'


class InventoryProfile(Profile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='inventory_profile')

    class Meta:
        verbose_name = 'Inventory Profile'
        verbose_name_plural = 'Inventories Profile'


class SupplyProfile(Profile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='supplier_profile')

    class Meta:
        verbose_name = 'Supplier Profile'
        verbose_name_plural = 'Suppliers Profile'


class DriverProfile(Profile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='driver_profile')

    class Meta:
        verbose_name = 'Driver Profile'
        verbose_name_plural = 'Drivers Profile'


class PackerProfile(Profile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='packer_profile')

    class Meta:
        verbose_name = 'Packer Profile'
        verbose_name_plural = 'Packers Profile'


class Conversation(models.Model):
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user1_conversations')
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user2_conversations')

    def __str__(self):
        return f'{self.user1.username} and {self.user2.username}'


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', null=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages', null=True)
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages', null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    email = models.EmailField(_('Sender Email'))

    def __str__(self):
        return f'From {self.sender.username} to {self.recipient.username}: {self.content[:50]}'


class Driver(CustomUser):
    pass

    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'


class Packer(CustomUser):
    pass

    class Meta:
        verbose_name = 'Packer'
        verbose_name_plural = 'Packers'


class Customer(CustomUser):
    pass

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Inventory(CustomUser):
    pass

    class Meta:
        verbose_name = 'Inventory'


class Finance(CustomUser):
    pass

    class Meta:
        verbose_name = 'Finance'
        verbose_name_plural = 'Finance'


class Supply(CustomUser):
    pass

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'


class FAQ(TimeStamp):
    class QustionType(models.TextChoices):
        CUSTOMER = 'CM', _('Customer')
        FINANCE = 'FM', _('Finance Manager')
        INVENTORY = 'IV', _('Inventory Manager')
        SUPPLY = 'SP', _('Supplier')
        DRIVER = 'DR', _('Driver')
        ALL = 'ALL', _('ALL')

    question_types = models.CharField(
        _('question Type'),
        max_length=3,
        # choices=QustionType.choices,
        # default=QustionType.CUSTOMER
    )
    subject = models.CharField(max_length=250, null=True)
    content = models.TextField(null=True)


class Aboutus(models.Model):
    verbose_name = 'About Us'

    content = models.TextField(max_length=1000)
