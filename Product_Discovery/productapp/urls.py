from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('',views.home,name='home'),
    path('deepsearch',views.deepsearch,name='deepsearch'),
    path('sparql', views.sparql, name='sparql'),
]
