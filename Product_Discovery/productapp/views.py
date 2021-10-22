from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView , LogoutView
from django.core.files.storage import FileSystemStorage

# Create your views here.

def home(request):
    return render(request, 'index.html')

def deepsearch(request):
    return render(request, 'deepsearch.html')

def sparql(request):
    return render(request, 'sparql.html')


def add(request):
    context = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)
            context['url'] = fs.url(name)
            return render(request, 'additems.html', context)
        return render(request, 'additems.html')
    else:
        return redirect('login/')

    

class Login(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

class LogOut(LogoutView):
    pass