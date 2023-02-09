from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

# Create your views here.
from accounts.forms import LoginForm, SignupForm


def register(request):
    msg = None
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login')
        else:
            msg = 'form is not valid'
    else:
        form = SignupForm()
    return render(request, 'register.html', {'form': form, 'msg': msg})


def login(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST" and form.is_valid():
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None and user.is_Admin:
                login(request, user)
                return redirect('admin')
            elif user is not None and user.is_Customer:
                login(request, user)
                return render('customer')
            else:
                msg = "Invalid Credentials"
        else:
            msg = "Error validating form"
    return render(request, 'login.html', {'form': form, 'msg': msg})


def reset(request):
    return render(request, 'reset.html')


def calendar(request):
    return render(request, 'calendar.html')


def customer(request):
    return render(request, 'customer.html')


def index(request):
    return render(request, 'index.html')
