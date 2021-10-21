from django.shortcuts import render
from django.contrib.auth.views import LoginView

# Create your views here.

def home(request):
    return render(request, 'index.html')

def deepsearch(request):
    return render(request, 'deepsearch.html')

def sparql(request):
    return render(request, 'sparql.html')
class Login(LoginView):
    template_name = "/registration/login.html"
    redirect_authenticed_user= True