# from django.contrib.auth.models import User
# from django.contrib.messages.views import SuccessMessageMixin
# from django.shortcuts import render, redirect
# from django.urls import reverse_lazy
# from django.views.generic import CreateView
# from accounts.forms import SignUpForm

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginForm, SignUpForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = None
            if username:
                user = authenticate(request, username=username, password=password)
            elif email:
                user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                # Redirect to the appropriate dashboard based on user selection
                dashboard = form.cleaned_data.get('dashboard')
                if dashboard == 'customer':
                    return redirect('customer_view')
                elif dashboard == 'inventory':
                    return redirect('inventory_view')
                elif dashboard == 'driver':
                    return redirect('driver_view')
                else:
                    return redirect('customer_view')  # Replace with your default dashboard view
            else:
                form.add_error(None, 'Invalid login credentials.')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = "register.html"
    form_class = SignUpForm
    model = User
    success_message = "You've registered successfully"
    success_url = reverse_lazy('accounts:login')


# def login(request):
#     return render(request, 'login.html')


def reset(request):
    return render(request, 'reset.html')


def calendar(request):
    return render(request, 'calendar.html')


def customer(request):
    return render(request, 'customer/index.html')


def icons(request):
    return render(request, 'icons.html')


def profile(request):
    return render(request, 'profile.html')
