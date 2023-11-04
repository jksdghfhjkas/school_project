import aiohttp
import json
from colorama import Fore
import asyncio
from time import ctime, time

import requests

HEADERS = [{'X-Yandex-API-Key': 'f9d5d3ab-ebde-4d39-8070-3e6f5ab81e8c'}, None]

URLS = ['https://api.weather.yandex.ru/v2/informers?lat={}&lon={}&lang=ru_RU', 
        'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=' + 'ae503a9e809c10ec2d6a2fdda6737a49' + '&units=metric']

SOURSE = ['Yandex api', 'OpenWeather api']

INFO_SITY = {'yandex': [], 'openweather': []}


def get_data_parser(source, name_sity, response_json, coord):

    if source == "Yandex api":
                
        print(Fore.GREEN + "Yandex" + Fore.WHITE)
        print(str(response_json), '\n\n\n')

    elif source == "OpenWeather api":

        print(Fore.GREEN + "Openwether" + Fore.WHITE)
        print(str(response_json), '\n\n\n')


TIME_COUNT = 0

async def Parser_Yandex_Weather(session, coord, header, url, source, name_sity, function):


    async with session.get(url.format(coord[0], coord[1]), proxy=None, headers=header) as response:

        if response.status == 200:
            response_json = json.loads(await response.text())
            if name_sity == None: name_sity = f'lat: {coord[0]}, lon: {coord[1]}'

            function(source, name_sity, response_json, coord) #функция разбора данных
    
        else: 
            print(Fore.RED + str(response.status) + Fore.WHITE)


async def Start_Parser(coordinates, name_sity, deskriptor):

    weather_task = []

    async with aiohttp.ClientSession() as session:
        for num, coord in enumerate(coordinates):
            weather_task.append(asyncio.create_task(Parser_Yandex_Weather(session, coord, header=None, url=URLS[1], source=SOURSE[1], name_sity=None, function=deskriptor)))
            weather_task.append(asyncio.create_task(Parser_Yandex_Weather(session, coord, header=HEADERS[0], url=URLS[0], source=SOURSE[0], name_sity=None, function=deskriptor)))
        await asyncio.gather(*weather_task)

asyncio.run(Start_Parser([[1, 1], [1, 1], [1, 1]], [None, None], get_data_parser))


 
   