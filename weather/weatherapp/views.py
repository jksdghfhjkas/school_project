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
from time import ctime

GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct?q={}&appid=" + 'ae503a9e809c10ec2d6a2fdda6737a49'

HEADERS = [{'X-Yandex-API-Key': 'f9d5d3ab-ebde-4d39-8070-3e6f5ab81e8c'}, None]

URLS = ['https://api.weather.yandex.ru/v2/informers?lat={}&lon={}&lang=ru_RU', 
        'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=' + 'ae503a9e809c10ec2d6a2fdda6737a49' + '&units=metric']

SOURSE = ['Yandex api', 'OpenWeather api']

INFO_SITY = {'yandex': [], 'openweather': []}


def get_data_parser(source, name_sity, response_json):

    if source == "Yandex api":
                
        INFO_SITY['yandex'].append({
            'city': name_sity,
            'temp': response_json['fact']['temp'],
            'date': ctime(),
            'image': 'http://127.0.0.1:8000/static/weatherapp/img/yandex_icon/{}.png'.format(response_json['fact']['icon']) 
        })

    elif source == "OpenWeather api":

        INFO_SITY['openweather'].append({
            'city': name_sity,
            'temp': response_json['main']['temp'],
            'date': ctime(),
            'image': response_json['weather'][0]['icon'],
        })



async def Parser_Yandex_Weather(session, coord, header, url, source, name_sity, function):


    async with session.get(url.format(coord[0], coord[1]), proxy=None, headers=header) as response:

        if response.status == 200:
            response_json = json.loads(await response.text())
            if name_sity == None: name_sity = f'lat: {coord[0]}, lon: {coord[1]}'

            function(source, name_sity, response_json) #функция разбора данных
    
        else: 
            print(Fore.RED + str(response.status) + Fore.WHITE)
            

async def Start_Parser(coordinates, name_sity, deskriptor):

    weather_task = []

    async with aiohttp.ClientSession() as session:
        for num, coord in enumerate(coordinates):
            
            weather_task += [asyncio.create_task(Parser_Yandex_Weather(session, 
                                                coord, 
                                                header=HEADERS[i], 
                                                url=URLS[i], 
                                                source=SOURSE[i], 
                                                name_sity=name_sity[num], 
                                                function=deskriptor)) for i in range(0, 2)]

            
        await asyncio.gather(*weather_task)

            

"""вывод страниц"""
def one_page(request):
    return render(request, "weatherapp/one_page.html")

@login_required
def Main(request):
    
    """обработка формы"""
    if request.method == "POST":

        # if str(request.POST.get('Delete')) != 'None':
        #     models.Sities.objects.filter(NameSity=request.POST.get('Delete')).delete()
        #     return redirect('main')

        
        form = forms.SitiesForm(request.POST)

        if form.is_valid():
            form.instance.user = request.user

            response = requests.get(GEOCODE_URL.format('London')).text
            response_json = json.loads(response)

            form.instance.coordinate_lat = response_json[0]['lat']
            form.instance.coordinate_lon = response_json[0]['lon']

            form.save()
            return redirect('main')
        
  
    cities = models.Sities.objects.filter(user=request.user)

    coordinate = [[i.coordinate_lat, i.coordinate_lon] for i in cities]
    set_namesity = [i.NameSity for i in cities]

    INFO_SITY['yandex'].clear()
    INFO_SITY['openweather'].clear()
    asyncio.run(Start_Parser(coordinate, name_sity=set_namesity, deskriptor=get_data_parser))

    form = forms.SitiesForm()
    return render(request, 'weatherapp/main.html', {'form': form, 'yandex': INFO_SITY['yandex'], 'openweather': INFO_SITY['openweather']})



def main(request):
    weather_shaman = ['Будет тепло', 'Будет холодно', 'Будет ветренно',
                      'Будет дождь', 'Будет солнечно', 'Будет ...', 'Не будет ...']

    if request.method == 'POST':

        INFO_SITY['yandex'].clear()
        INFO_SITY['openweather'].clear()
        
        if request.POST.get('NameSity') != None:
            sity = request.POST.get('NameSity')
            response = requests.get(GEOCODE_URL.format('London')).text
            response_json = json.loads(response)

            coord = [response_json[0]['lat'],
                     response_json[0]['lon']]
            
            asyncio.run(Start_Parser(coord, sity))

        elif request.POST.get('lat') != '' and request.POST.get('lon') != '': 

            lat = int(request.POST.get('lat'))
            lon = int(request.POST.get('lon'))

            asyncio.run(Start_Parser([[lat, lon]], [None], get_data_parser))

        return redirect('one_page')

    return render(request, 'weatherapp/main-two.html', {'shaman': choice(weather_shaman), 'info_openweather': INFO_SITY['openweather'], 'info_yandex': INFO_SITY['yandex']})



#forecast render template >>>>

from django.views.generic import DetailView

class NewsDetailViews(DetailView):
    model = models.Sities
    template_name = 'forecast/weather_forecast_open.html'
    context_object_name = 'name_sity'


URLS[0] = None
URLS[1] = "api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid=" + 'ae503a9e809c10ec2d6a2fdda6737a49' + '&units=metric'


def get_forecast_openweather(name_sity, response_json):
    pass


@login_required
def forecast_openweather(request):

    asyncio.run(Start_Parser([[1, 1]], [None], get_data_parser))


    return render(request, 'weatherapp/weather_forecast_open.html')

@login_required
def forecast_yandex(request):
    return render(request, 'weatherapp/weather_forecast_yandex.html')
