from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='one_page'),
    path('main/', views.Weather_login_get, name='main'),
    path('forecast/', views.forecast, name='forecast')
]
