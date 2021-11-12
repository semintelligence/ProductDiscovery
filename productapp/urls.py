from django.urls import path, include
from . import views

urlpatterns = [
    path('login/',views.Login.as_view()),
    path('logout/',views.LogOut.as_view(),name='logout'),
    path('',views.home,name='home'), 
    path('deepsearch',views.deepsearch,name='deepsearch'),
    path('sparql', views.sparql, name='sparql'),
    path('add', views.add, name="add"),
    path('search',views.search,name="search"),
    path('query',views.query,name="query")
]
