from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

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
            elif user.user_type not in ['FM', 'DR', 'SP', 'IV', 'CM', 'PC']:
                self.add_error(None, forms.ValidationError(" Please register first."))

        return self.cleaned_data


