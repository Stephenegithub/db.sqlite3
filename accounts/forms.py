from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, logout
from django.forms import forms
from django import forms

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
            if self.user_cache is not None and self.user_cache.is_staff or self.user_cache.user_type == "DR" or \
                    self.user_cache.user_type == "FM" or self.user_cache.user_type == "SP" or \
                    self.user_cache.user_type == "IV":
                logout(self.request)
                raise forms.ValidationError('Invalid username or password for customer login', code='invalid login')
