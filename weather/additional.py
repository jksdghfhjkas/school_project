import aiohttp
import json
from colorama import Fore
import asyncio
from time import ctime

import requests

HEADERS = [{'X-Yandex-API-Key': 'f9d5d3ab-ebde-4d39-8070-3e6f5ab81e8c'}, None]

URLS = ['https://api.weather.yandex.ru/v2/informers?lat={}&lon={}&lang=ru_RU', 
        'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=' + 'ae503a9e809c10ec2d6a2fdda6737a49' + '&units=metric']

SOURSE = ['Yandex api', 'OpenWeather api']

INFO_SITY = {'yandex': [], 'openweather': []}


def get_data_parser(source, name_sity, response_json):

    if source == "Yandex api":
                
        print(Fore.GREEN + "Yandex" + Fore.WHITE)
        print(str(response_json), '\n\n\n')

    elif source == "OpenWeather api":

        print(Fore.GREEN + "Openwether" + Fore.WHITE)
        print(str(response_json), '\n\n\n')



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

    
# asyncio.run(Start_Parser([[1, 1], [1, 1]], [None, None], get_data_parser))

URL = 'api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid=' + 'ae503a9e809c10ec2d6a2fdda6737a49'

response = requests.get(URL.format(1, 1))
