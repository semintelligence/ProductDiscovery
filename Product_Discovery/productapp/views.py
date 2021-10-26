from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView , LogoutView
from django.core.files.storage import FileSystemStorage
import requests

# Create your views here.

def home(request):
    return render(request, 'index.html')

def deepsearch(request):
    if(request.method == 'POST'):
        category  = "=" + request.POST.get('category')
        brand  = "=" +request.POST.get('brand')
        ram  = "=" +request.POST.get('ram')
        operatingsystem  = "=" +request.POST.get('operatingsystem')
        priceineuros  = "=" +request.POST.get('priceineuros')
        quantity  = "=" +request.POST.get('quantity')
        seller  = "=" +request.POST.get('seller')
        cpu  = "=" +request.POST.get('cpu')
        gpu  = "=" +request.POST.get('gpu')
        screensize  = "=" +request.POST.get('screensize')
        screentype  = "=" +request.POST.get('screentype')
        storage  = "=" +request.POST.get('storage')
        url = "https://product-discovery-service.herokuapp.com/recommendProduct?Category"+category+"&Brand" + brand + "&RAM" + ram + "&OperatingSystem" +operatingsystem +"&PriceInEuros" + priceineuros + "&Quantity" + quantity + "&Seller" + seller + "&CPU" + cpu + "&GPU" + gpu + "&ScreenSize" + screensize + "&ScreenType"+screentype+"&Storage" + storage
        res = requests.get(url)
        resList = res.text.split(',')
        return render(request,'deepsearchproduct.html')
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