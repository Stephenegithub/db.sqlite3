from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView

from .forms import SignUpForm, CustomerAuthenticationForm, CustomUser


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = "register.html"
    form_class = SignUpForm
    model = User
    success_message = "You've registered successfully"
    success_url = reverse_lazy('accounts:login')


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You've registered successfully")
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.method == 'POST':
        form = CustomerAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomerAuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def dashboard(request):
    user_type = request.user

    if user_type == CustomUser.UserTypes.FINANCE:
        return render(request, 'finance/index.html')
    elif user_type == CustomUser.UserTypes.DRIVER:
        return render(request, 'driver/index.html')
    elif user_type == CustomUser.UserTypes.SUPPLIER:
        return render(request, 'suppliers/index.html')
    elif user_type == CustomUser.UserTypes.INVENTORY:
        return render(request, 'inventory/index.html')
    elif user_type == CustomUser.UserTypes.CUSTOMER:
        return render(request, 'customer/index.html')
    elif user_type == CustomUser.UserTypes.PACKERS:
        return render(request, 'packer/index.html')

    return render(request, 'dashboard/dashboard.html')


def user_logout(request):
    logout(request)
    return redirect('login')


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
