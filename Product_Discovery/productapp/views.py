from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView , LogoutView
from django.core.files.storage import FileSystemStorage
import requests

# Create your views here.

def home(request):
    return render(request, 'index.html')

def search(request):
    keyword = request.POST.get("keyword1")
    if(keyword==""): keyword = request.POST.get("keyword2")
    url = "https://product-discovery-service.herokuapp.com/rapidInformationExplorer?keyword="+keyword
    result = requests.get(url)
    result = result.text.split(',')
    # left here
    return render(request, "res.html")


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
        resList = requests.get(url)
        resList = resList.text.split(',')
        modelNo = []
        name = []
        price = []
        image = []
        for item in resList:
            index1 = item.find("?ProductModelNo = ") + len("?ProductModelNo = ")
            index2 = index1 + item[index1:].find(">")
            modelNo.append(item[index1:index2+1])  
            index1 = item.find("?ProductName = ")  + len("?ProductName = ")
            index2 = index1 + item[index1+2:].find(chr(92))
            res = item[index1 + 2:index2+1]
            if(res.find("(")): res = res.replace("(","")
            name.append(res)
            index1 = item.find("?Price = ") + len("?Price = ")
            index2 = index1 + item[index1:].find('"')
            temp = item[index2+2:index2+12]
            index3 = temp.find("^")
            price.append(item[index2+1:index2+index3])
            index1 = item.find("?Image = ") + len("?Image = ")
            index2 = index1 + item[index1:].find(")")
            image.append(item[index1+1:index2-2])
        res = {
            'result': zip(modelNo, name ,price,image)
        }
        return render(request,'deepsearchproduct.html',context=res)
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