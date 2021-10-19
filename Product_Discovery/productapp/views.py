from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'index.html')

def deepsearch(request):
    return render(request, 'deepsearch.html')

def sparql(request):
    return render(request, 'sparql.html')

def login(request):
    return render(request, 'login.html')