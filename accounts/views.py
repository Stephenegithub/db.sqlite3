from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import SignUpForm


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = "register.html"
    form_class = SignUpForm
    model = User
    success_message = "You've registered successfully"
    success_url = reverse_lazy('accounts:login')


def login(request):
    return render(request, 'login.html')


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
