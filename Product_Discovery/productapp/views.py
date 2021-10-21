from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView , LogoutView
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    return render(request, 'index.html')

def deepsearch(request):
    return render(request, 'deepsearch.html')

def sparql(request):
    return render(request, 'sparql.html')

def add(request):
    if request.user.is_authenticated:
        return render(request, 'additems.html')
    return redirect('login/')

class Login(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

class LogOut(LogoutView):
    pass