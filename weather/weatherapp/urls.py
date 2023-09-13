from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('main/', views.Main, name='main') 
]
