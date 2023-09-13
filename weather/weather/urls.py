
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from userlogin import views as userlogin_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("weatherapp.urls")),
    

    #userlogin register url
    path('register/', userlogin_views.registr, name='registr'),
    path('login/', auth_views.LoginView.as_view(template_name='userlogin/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='userlogin/logout.html'), name='logout'),
]


