from django.shortcuts import render


# Create your views here.
def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def reset(request):
    return render(request, 'reset.html')

def calendar(request):
    return render(request, 'calendar.html')