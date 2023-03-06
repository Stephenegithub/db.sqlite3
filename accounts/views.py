from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import SignUpForm, LoginForm, CustomUser


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = "register.html"
    form_class = SignUpForm
    model = User
    success_message = "You've registered successfully"
    success_url = reverse_lazy('accounts:login')


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, CustomUser)
                return redirect('admin')
            elif user is not None and user.is_customer:
                login(request, CustomUser)
                return redirect('customer')
            elif user is not None and user.is_employee:
                login(request, CustomUser)
                return redirect('employee')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})


def reset(request):
    return render(request, 'reset.html')


def calendar(request):
    return render(request, 'calendar.html')


def login(request):
    return render(request, 'login.html')


def customer(request):
    return render(request, 'customer.html')


def index(request):
    return render(request, 'index.html')


def icons(request):
    return render(request, 'icons.html')


def profile(request):
    return render(request, 'profile.html')


def product(request):
    return render(request, 'product.html')


def order(request):
    return render(request, 'order.html')
