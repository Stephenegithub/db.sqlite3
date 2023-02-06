from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return render(request, "index.html")


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def login(request):
    if request.method == 'POST':
        useremail = request.POST['useremail']
        password = request.POST['password']
        user = authenticate(request, username=useremail, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('success')
        else:
            # Return an 'invalid login' error message.
            return redirect('login')
    return render(request, 'login.html')
