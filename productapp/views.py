from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView , LogoutView
import requests
import re
import numpy as np
from django.urls import reverse


# Create your views here.

def home(request):
    return render(request, 'index.html')

def search(request):
    keyword = request.POST.get("keyword1")
    if(keyword==""): keyword = request.POST.get("keyword2")
    url = "https://product-discovery-service.herokuapp.com/rapidInformationExplorer?keyword="+keyword
    result = requests.get(url)
    result = result.text.split(',')
    modelNo = []
    name = []
    price = []
    image = []
    for item in result:
        image.append("https://source.unsplash.com/featured/?" +str(len(name)))
        index1 = item.find("?Subject = <") + len("?Subject = <")
        index2 = item.find("> ) ( ?P")
        modelNo.append(item[index1:index2])
        index1 = item.find("( ?Property = <") + len("( ?Property = <")
        index2 = item.find("> ) ( ?O")
        name.append(item[index1:index2])
        index1 = item.find("?Object = ") + len("?Object = ")
        index2 = index1 + item[index1+2:].find(chr(92))
        res = item[index1+2:index2+2]
        if(res.find("(")): res = res.replace("(","")
        if(res.find(")")): res = res.replace(")","")
        price.append(res)
    res = {
            'result': list(zip(modelNo, name ,price,image))
        }
    return render(request, "deepsearchproduct.html", context=res)


def deepsearch(request):
    if(request.method == 'POST'):
        if(request.POST.get("method") == "sort"):
            model = request.POST.get("products")
            method = request.POST["option"] == "sortA"
            model,name,price,image = zip(*eval(model))
            model = list(model)
            name  = list(name)
            price = list(price)
            image = list(image)  
            if(method):
                arg = np.argsort(price)
            else:
                arg = np.argsort(price)[::-1]
            price = list(np.array(price)[arg])
            name = list(np.array(name)[arg])
            image = list(np.array(image)[arg])
            model = list(np.array(model)[arg])
            minimum = int(request.POST.get("min"))
            maximum = int(request.POST.get("max"))
            res = {
                'result': list(zip(model, name ,price,image)),
                'minimum': minimum,
                'maximum': maximum
            }
        else:
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
                res = item[index1 + 2:index2+2]
                if(res.find("(")): res = res.replace("(","")
                if(res.find(")")): res = res.replace(")","")
                name.append(res)
                index1 = item.find("?Price = ") + len("?Price = ")
                index2 = index1 + item[index1:].find('"')
                temp = item[index2+2:index2+12]
                index3 = temp.find("^")
                price.append(item[index2+1:index2+index3])
                index1 = item.find("?Image = ") + len("?Image = ")
                index2 = index1 + item[index1:].find(")")
                # image.append(item[index1+1:index2-2])
                image.append("https://source.unsplash.com/featured/?" +str(len(name))) # temp for images
            price = [float(re.findall(r"[-+]?\d*\.\d+|\d+", i)[0]) for i in price] # converting list of string to list of float using regular expression
            minimum = int(min(price))
            maximum = int(max(price))
            res = {
                'result': list(zip(modelNo, name ,price,image)),
                'minimum': minimum,
                'maximum': maximum
            }
        return render(request,'deepsearchproduct.html',context=res)
    else:
        return render(request, 'deepsearch.html')

def sparql(request):
    if request.method == 'POST':
        if(request.POST.get("method") == "sort"):
            model = request.POST.get("products")
            method = request.POST["option"] == "sortA"
            model,name,price,image = zip(*eval(model))
            model = list(model)
            name  = list(name)
            price = list(price)
            image = list(image)  
            if(method):
                arg = np.argsort(price)
            else:
                arg = np.argsort(price)[::-1]
            price = list(np.array(price)[arg])
            name = list(np.array(name)[arg])
            image = list(np.array(image)[arg])
            model = list(np.array(model)[arg])
            minimum = int(request.POST.get("min"))
            maximum = int(request.POST.get("max"))
            res = {
                'result': list(zip(model, name ,price,image)),
                'minimum': minimum,
                'maximum': maximum
            }
        else:
            url = "https://product-discovery-service.herokuapp.com/sparqlEndpoint"
            query = request.POST.get("main_query")
            res = requests.post(url,data=query)
            if(res.status_code   == 500):
                return render(request, 'sparql.html', context={'flag': True, 'msg': "something went wrong"})
            model = []
            name = []
            price = []
            image = []
            res = res.text.split(',')
            for item  in res:
                image.append("https://source.unsplash.com/featured/?" +str(len(name))) # temp for images
                index1 = item.find("?ProductName = ") + len("?ProductName = ") +2
                index2 = item.find('" ) ( ?B') -1
                model.append(item[index1:index2])
                index1 = item.find('''?Brand = <http://rdf-dump/eeo/0.1/''') + len('''?Brand = <http://rdf-dump/eeo/0.1/''')
                index2 = item.find("> ) ( ?Seller")
                name.append(item[index1:index2])
                index1 = item.find("?Price = ") + len("?Price = ")
                index2 = index1 + item[index1:].find('"')
                temp = item[index2+2:index2+12]
                index3 = temp.find("^")
                price.append(item[index2+1:index2+index3])
        price = [float(re.findall(r"[-+]?\d*\.\d+|\d+", i)[0]) for i in price] # converting list of string to list of float using regular expression
        minimum = int(min(price))
        maximum = int(max(price))
        res = {
            'result': list(zip(model, name ,price,image)),
            'minimum': minimum,
            'maximum': maximum
        }
        return render(request,'deepsearchproduct.html',context=res)
    return render(request, 'sparql.html')


def add(request):   
    context = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            uploaded_file = request.FILES['document']
            url = "https://product-discovery-service.herokuapp.com/uploadProductCatalog"
            r = requests.post(url,files={"file": uploaded_file})
            context = {"flag": True,"responce": r.text}
            return render(request, 'additems.html', context)
        context = {"flag": False}  
        return render(request, 'additems.html',context)
    else:
        return redirect('login/')

class Login(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

class LogOut(LogoutView):
    pass

def query(request):
    return render(request,'query.html')