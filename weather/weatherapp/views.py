#django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import models
from . import forms

#parsing
import requests
import json
import asyncio
import aiohttp
from datetime import date


GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct?q={}&appid=" + 'token_api_openweather'

HEADERS = [{'X-Yandex-API-Key': 'token_api_yandex'}, None]

URLS = ['https://api.weather.yandex.ru/v2/informers?lat={}&lon={}&lang=ru_RU', 
        'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=' + 'token_api_openweather' + '&units=metric&lang=ru']

SOURSE = ['Yandex api', 'OpenWeather api']

INFO_SITY = {'yandex': [], 'openweather': [], 'Error': None}

TRANSLATOR = {"clear": "ясно",
    "partly-cloudy": "малооблачно",
    "cloudy": "облачно с прояснениями",
    "overcast": "пасмурно",
    "light-rain": "небольшой дождь",
    "rain": "дождь",
    "heavy-rain": "сильный дождь",
    "showers": "ливень",
    "wet-snow": "дождь со снегом",
    "light-snow": "небольшой снег",
    "snow": "снег",
    "snow-showers": "снегопад",
    "hail": "град",
    "thunderstorm": "гроза",
    "thunderstorm-with-rain": "дождь с грозой",
    "hunderstorm-with-hail": "гроза с градом"
}


def Transcript(source, name_sity, response_json, coord):
    global TRANSLATOR

    date_return = str(date.today())

    if source == "Yandex api":
        INFO_SITY['yandex'].append({
            'city': name_sity,
            'temp': response_json['fact']['temp'],
            'date': date_return,
            'image': response_json['fact']['icon'],
            'cloud': TRANSLATOR.get(response_json['fact']['condition']),
            'wind': response_json['fact']['wind_speed']
        })

    elif source == "OpenWeather api":

        INFO_SITY['openweather'].append({
            'city': name_sity,
            'temp': response_json['main']['temp'],
            'date': date_return,
            'image': response_json['weather'][0]['icon'],
            'wind' : response_json['wind']['speed'],
            'cloud' : response_json['weather'][0]['description']
        })




async def Parser_Weather(session, coord, header, url, source, name_sity, function):

    try:
        async with session.get(url.format(*coord), proxy=None, headers=header, timeout=100) as response:

            if response.status == 200:
                response_json = json.loads(await response.text())
                if name_sity == None: name_sity = f'lat: {coord[0]}, lon: {coord[1]}'

                function(source, name_sity, response_json, coord) #функция разбора данных
            
            else: 
                print(str(response.status))
    except:
        print('Error')
    

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
    if INFO_SITY['openweather'] != None:
        INFO_SITY['yandex'].clear()
        INFO_SITY['openweather'].clear()
    
    """обработка формы"""
    if request.method == "POST":
        if request.POST.get('add', None):
            form = forms.SitiesForm(request.POST)

            if form.is_valid():
                form.instance.user = request.user

                response = requests.get(GEOCODE_URL.format(request.POST.get('NameSity')))
                
                if response.status_code == 200 and response.text != '[]':
                    
                    response_json = json.loads(response.text)

                    form.instance.coordinate_lat = response_json[0]['lat']
                    form.instance.coordinate_lon = response_json[0]['lon']

                    form.save()
                return redirect('main')
            
        elif request.POST.get('del', None):
            form_del = forms.DeleteSitiesForm(request.POST, user=request.user)

            if form_del.is_valid():
                form_del.cleaned_data['record'].delete()
  

    cities = models.Sities.objects.filter(user=request.user)

    coordinate = [[i.coordinate_lat, i.coordinate_lon] for i in cities]
    set_namesity = [i.NameSity for i in cities]

    asyncio.run(Start_Parser(coordinate, name_sity=set_namesity, transcript=Transcript))

    form_del = forms.DeleteSitiesForm(user=request.user)
    form = forms.SitiesForm()
    return render(request, 'weatherapp/main.html', {'form': form,
                                                    'form_del': form_del,
                                                    'yandex': INFO_SITY['yandex'],
                                                    'openweather': INFO_SITY['openweather']})

def main(request):

    if len(INFO_SITY['openweather']) > 1:
        INFO_SITY['yandex'].clear()
        INFO_SITY['openweather'].clear()

    if request.method == 'POST':

        if INFO_SITY['openweather'] != None:
            INFO_SITY['yandex'].clear()
            INFO_SITY['openweather'].clear()
        
        if request.POST.get('NameSity') != None:
            sity = request.POST.get('NameSity')
            response = requests.get(GEOCODE_URL.format(sity))

            if response.status_code == 200 and response.text != '[]':

                response_json = json.loads(response.text)

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

from itertools import groupby

ForeCast_URL = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid=' + 'ae503a9e809c10ec2d6a2fdda6737a49' + '&units=metric&lang=ru'
FORECAST_INFO = {'days': [], 'info': []}

MONTHS = [
 'январь',
 'февраль',
 'март',
 'апрель',
 'май',
 'июнь',
 'июль',
 'август',
 'сентябрь',
 'октябрь',
 'ноябрь',
 'декабрь']

def Transcript_forecast(response_json, name_sity):
    global FORECAST_INFO

    FORECAST_INFO['days'] = [{'day': day.split("-")[1],
                              'mount': MONTHS[int(day.split("-")[0])]}
                              for day, _ in groupby([value['dt_txt'][5:10] for value in response_json['list']])]

    FORECAST_INFO['info'] = [{
        'sity': name_sity,
        'temp': value['main']['temp'],
        'image': value['weather'][0]['icon'],
        'wind' : value['wind']['speed'],
        'cloud' : value['weather'][0]['description'],
        'day': value['dt_txt'][8:10],
        'time': value['dt_txt'][10:16] 
        
    } for value in response_json['list']] 



def Forecast_Parser(coordinate, namesity):
    response = requests.get(ForeCast_URL.format(*coordinate))
    if response.status_code == 200:
        response_json = json.loads(response.text)
        if namesity == None: namesity = f'lat: {coordinate[0]}, long: {coordinate[1]}'
        Transcript_forecast(response_json, namesity)
    
    else: 
        print(str(response.status_code))

def forecast(request):

    if FORECAST_INFO['days'] != None:
        FORECAST_INFO['info'].clear()
        FORECAST_INFO['days'].clear()

    if request.method == 'GET':
        sity = request.GET.get('sity')
        lat, long = request.GET.get('lat'), request.GET.get('long')

        if sity != None:

            response = requests.get(GEOCODE_URL.format(sity))
            if response.status_code == 200 and response.text != '[]':

                response_json = json.loads(response.text)

                coord = [response_json[0]['lat'],
                        response_json[0]['lon']]
                
                Forecast_Parser(coord, sity)

        elif lat != None and long != None:
            Forecast_Parser([lat, long], None)
    
    return render(request, 'weatherapp/forecast.html', {'info': FORECAST_INFO})

