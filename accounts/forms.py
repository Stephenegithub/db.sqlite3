from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
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


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control"
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )

    # def clean(self):
    #     data = super().clean()
    #     username = data.get("username")
    #     password = data.get("password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = CustomUser.objects.filter(username__iexact=username)  # thisIsMyUsername == this is my username
        if not qs.exists():
            raise forms.ValidationError("This is an invalid user.")
        if qs.count() != 1:
            raise forms.ValidationError("This is an invalid user.")
        return username
