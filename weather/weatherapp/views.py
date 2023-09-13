from django.shortcuts import render, redirect
import requests
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
from colorama import Fore

import json
import asyncio
import aiohttp

from django.contrib.auth.models import User

from random import choice


URL = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + 'ae503a9e809c10ec2d6a2fdda6737a49'
USER_SITY = []

"""асинхронный парсер погоды"""
async def Request_Get_Weather(city, session):
    async with session.get(URL.format(city), proxy=None) as response:
        response_json = json.loads(await response.text())
        
        if response_json['cod'] != '404':

            USER_SITY.append({
                'city': city,
                'temp': response_json['main']['temp'],
                'image': response_json['weather'][0]['icon']
            })

async def Request_User_Weather(cityes):
    city_tasks = []
    async with aiohttp.ClientSession() as session:
        for city in cityes:
            city_tasks.append(asyncio.create_task(Request_Get_Weather(city, session)))
        await asyncio.gather(*city_tasks)




"""вывод страниц"""
def one_page(request):
    return render(request, "weatherapp/one_page.html")

@login_required
def Main(request):

    """обработка формы"""
    if request.method == "POST":
        # print(Fore.GREEN + str(request.POST.get('Delete')) + Fore.WHITE)

        if str(request.POST.get('Delete')) != 'None':
            models.Sities.objects.filter(NameSity=request.POST.get('Delete')).delete()
            return redirect('main')

        else:
          
            form = forms.SitiesForm(request.POST)
            code = requests.get(URL.format(request.POST.get('NameSity'))).status_code
            # print(Fore.GREEN + str(code) + Fore.WHITE)

            if form.is_valid() and code == 200:
                form.instance.user = request.user
                form.save()
                return redirect('main')
        
  
    cities = models.Sities.objects.filter(user=request.user)
    USER_SITY.clear()
    asyncio.run(Request_User_Weather(cities))

    form = forms.SitiesForm()
    return render(request, 'weatherapp/main.html', {'form': form, 'user_sity': USER_SITY})

def main(request):
    weather_shaman = ['Будет тепло', 'Будет холодно', 'Будет ветренно',
                      'Будет дождь', 'Будет солнечно', 'Будет ...', 'Не будет ...']

    

    return render(request, 'weatherapp/main-two.html', {'shaman': choice(weather_shaman)})
