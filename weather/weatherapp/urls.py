from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='one_page'),
    path('main/', views.Weather_login_get, name='main'),
    path('forecast/yandex/', views.forecast_yandex, name='five_day_yandex'),
    path('forecast/open/<str:id_sity>/', views.forecast_openweather, name='fore-open')
]
