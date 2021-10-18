from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'index.html')

def deepsearch(request):
    return render(request, 'deepsearch.html')