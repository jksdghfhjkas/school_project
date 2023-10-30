from django.shortcuts import render, redirect
import requests
from django.contrib.auth.decorators import login_required
from . import models
from django.db.models import Q
from . import forms
from colorama import Fore
from django.contrib.auth.models import User

import json
import asyncio
import aiohttp

from time import ctime
from translate import Translator


def Print(string):
    print(Fore.GREEN + str(string) + Fore.WHITE)


GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct?q={}&appid=" + 'ae503a9e809c10ec2d6a2fdda6737a49'

HEADERS = [{'X-Yandex-API-Key': 'f9d5d3ab-ebde-4d39-8070-3e6f5ab81e8c'}, None]

URLS = ['https://api.weather.yandex.ru/v2/informers?lat={}&lon={}&lang=ru_RU', 
        'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=' + 'f2319986030c77f8d17c87999e88be66' + '&units=metric']

SOURSE = ['Yandex api', 'OpenWeather api']

INFO_SITY = {'yandex': [], 'openweather': []}

TRANSLATOR = Translator(to_lang="Russian")

def Test_Transcript(source, name_sity, response_json, coord):
    print(Fore.GREEN + str(response_json) + Fore.WHITE)

def Transcript(source, name_sity, response_json, coord):
    global TRANSLATOR

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
            'wind' : response_json['wind']['speed'],
            'cloud' : TRANSLATOR.translate(response_json['weather'][0]['main'])
        })




async def Parser_Weather(session, coord, header, url, source, name_sity, function):


    async with session.get(url.format(*coord), proxy=None, headers=header, timeout=100) as response:

        if response.status == 200:
            response_json = json.loads(await response.text())
            if name_sity == None: name_sity = f'lat: {coord[0]}, lon: {coord[1]}'

            function(source, name_sity, response_json, coord) #функция разбора данных
    
        else: 
            print(Fore.RED + str(response.status) + Fore.WHITE)
            

async def Start_Parser(coordinates, name_sity, transcript):

    weather_task = []

    async with aiohttp.ClientSession() as session:
        for num, coord in enumerate(coordinates):
            
            weather_task += [asyncio.create_task(Parser_Weather(session, 
                                                coord, 
                                                header=HEADERS[i], 
                                                url=URLS[i], 
                                                source=SOURSE[i], 
                                                name_sity=name_sity[num], 
                                                function=transcript)) for i in range(0, 2)]

            
        await asyncio.gather(*weather_task)

            
"""вывод страниц"""

@login_required
def Weather_login_get(request):
    
    """обработка формы"""
    if request.method == "POST":

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
    asyncio.run(Start_Parser(coordinate, name_sity=set_namesity, transcript=Test_Transcript))

    form = forms.SitiesForm()
    return render(request, 'weatherapp/main.html', {'form': form, 'yandex': INFO_SITY['yandex'], 'openweather': INFO_SITY['openweather']})



def main(request):

    if request.method == 'POST':
        INFO_SITY['yandex'].clear()
        INFO_SITY['openweather'].clear()


        if request.POST.get('NameSity') != None:
            sity = request.POST.get('NameSity')
            response = requests.get(GEOCODE_URL.format(sity)).text
            response_json = json.loads(response)

            coord = [response_json[0]['lat'],
                     response_json[0]['lon']]

            asyncio.run(Start_Parser([coord], [sity], Transcript))

        elif request.POST.get('lat') != '' and request.POST.get('lon') != '': 

            lat = int(request.POST.get('lat'))
            lon = int(request.POST.get('lon'))

            asyncio.run(Start_Parser([[lat, lon]], [None], Transcript))

        return redirect('one_page')

    return render(request, 'weatherapp/main-two.html', {'info_openweather': INFO_SITY['openweather'], 'info_yandex': INFO_SITY['yandex']})



#forecast render template >>>>

ForeCast_URL = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid=' + 'ae503a9e809c10ec2d6a2fdda6737a49' + '&units=metric'
FORECAST_INFO = []


def Transcript_forecast(source, name_sity, response_json, coord):
    global FORECAST_INFO
    FORECAST_INFO.append(response_json)

async def Forecast_Start_Parser(coordinate, namesity):
    async with aiohttp.ClientSession() as session:
        
        await asyncio.gather(asyncio.create_task(Parser_Weather(session, 
                                                                coord=coordinate,
                                                                url=ForeCast_URL,
                                                                header=None,
                                                                source=None,
                                                                name_sity=namesity,
                                                                function=Transcript_forecast)))


def forecast(request):

    if request.method == 'GET':
        FORECAST_INFO.clear()
        sity = request.GET.get('sity')
        lat, long = request.GET.get('lat'), request.GET.get('long')    

        if sity != None:
            response = requests.get(GEOCODE_URL.format(sity))
            if response.status_code == 200:

                response_json = json.loads(response.text)

                coord = [response_json[0]['lat'],
                        response_json[0]['lon']]

                asyncio.run(Forecast_Start_Parser(coord, sity))

        elif lat != None and long != None:
            asyncio.run(Forecast_Start_Parser([lat, long], None))
    
    return render(request, 'weatherapp/forecast.html', {'info': FORECAST_INFO})


@login_required
def forecast_openweather(request, id_sity):
    if id_sity != 'none':
        id_sity = False

        cities = models.Sities.objects.filter(Q(user=request.user) and Q(NameSity=id_sity))[0]
        coordinate = [cities.coordinate_lat, cities.coordinate_lon]
        asyncio.run(Forecast_Start_Parser(coordinate, cities.NameSity))
        
    else: id_sity = True

    return render(request, 'weatherapp/weather_forecast_open.html', {'info' : FORECAST_INFO, 'none': id_sity})

@login_required
def forecast_yandex(request):
    return render(request, 'weatherapp/weather_forecast_yandex.html')
