from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import *

CustomUser = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "CM"
        if commit:
            user.save()
        return user


class CustomerAuthenticationForm(AuthenticationForm):
    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                self.add_error('username', forms.ValidationError("Invalid username or password."))
            elif user.user_type not in ['FM', 'DR', 'SP', 'IV', 'CM', 'DM', 'PC']:
                self.add_error(None, forms.ValidationError(" Please register first."))

        return self.cleaned_data


class UserAdminChangeForm(ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admins
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'is_active']

    def clean_username(self):
        data = self.cleaned_data['username']
        return data.upper()

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class CustomerProfileForm(ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['image', 'gender']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['last_name', 'first_name', 'email']


class SupplierProfileForm(ModelForm):
    class Meta:
        model = SupplyProfile
        fields = ['image', 'gender']


class SupplyForm(ModelForm):
    class Meta:
        model = Supply
        fields = ['last_name', 'first_name', 'email']


class DriverProfileForm(ModelForm):
    class Meta:
        model = DriverProfile
        fields = ['image', 'gender', ]


class DriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = ['last_name', 'first_name', 'email']


class PackerProfileForm(ModelForm):
    class Meta:
        model = PackerProfile
        fields = ['image', 'gender', ]


class PackerForm(ModelForm):
    class Meta:
        model = Packer
        fields = ['last_name', 'first_name', 'email']


class FinanceProfileForm(ModelForm):
    class Meta:
        model = FinanceProfile
        fields = ['image', 'gender']


class FinanceForm(ModelForm):
    class Meta:
        model = Finance
        fields = ['last_name', 'first_name', 'email']


class InventoryProfileForm(ModelForm):
    class Meta:
        model = InventoryProfile
        fields = ['image', 'gender']


class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['last_name', 'first_name', 'email']


from django import forms
from .models import Conversation, Message


class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['user2']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'placeholder': 'Type your message here...'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email address...'})
