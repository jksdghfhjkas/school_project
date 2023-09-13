from django.shortcuts import render, redirect
from . import forms
from django.contrib import messages

def index(request):
    return render(request, "userlogin/index.html")

def registr(request):
    if request.method == "POST":
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('login')
        
    else:
        form = forms.UserRegisterForm()
        return render(request, 'userlogin/registr.html', {'form': form})


        





