import requests 
import json
from bs4 import BeautifulSoup
from colorama import Fore

from time import ctime

import asyncio
import aiohttp

GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct?q={}&appid=" + 'ae503a9e809c10ec2d6a2fdda6737a49'

HEADERS = [{'X-Yandex-API-Key': 'f9d5d3ab-ebde-4d39-8070-3e6f5ab81e8c'}, None]

URLS = ['https://api.weather.yandex.ru/v2/informers?lat={}&lon={}&lang=ru_RU', 
        'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=' + 'ae503a9e809c10ec2d6a2fdda6737a49' + '&units=metric']

SOURSE = ['Yandex api', 'OpenWeather api']

INFO_SITY = {'yandex': [], 'openweather': []}


async def Parser_Yandex_Weather(session, coord, header, url, source, name_sity):
    async with session.get(url.format(coord[0], coord[1]), proxy=None, headers=header) as response:

        if response.status == 200:
            response_json = json.loads(await response.text())


            if name_sity == None: name_sity = f'lat: {coord[0]}, lon: {coord[1]}'

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
    
        else: 
            print(Fore.RED + str(response.status) + Fore.WHITE)
            

async def Start_Parser(coordinates, name_sity=None, set=True):

    weather_task = []
    if set:
        async with aiohttp.ClientSession() as session:
            for num, coord in enumerate(coordinates):
                weather_task += [asyncio.create_task(Parser_Yandex_Weather(session, 
                                                                        coord, 
                                                                        header=HEADERS[i],
                                                                        url=URLS[i],
                                                                        source=SOURSE[i],
                                                                        name_sity=name_sity)) for i in range(0, 2)]
            await asyncio.gather(*weather_task)


asyncio.run(Start_Parser([[1, 1], [1, 1]]))
